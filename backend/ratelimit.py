"""In-memory limiter for failed login attempts.

State lives in the process, which fits the single-instance deployment this app
targets. Running several workers or instances would need a shared store
(for example Redis) to keep the limit global.
"""

import threading
import time
from collections import deque


class FailedLoginLimiter:
    def __init__(self, max_attempts: int, window_seconds: int, clock=time.monotonic):
        self.max_attempts = max_attempts
        self.window = window_seconds
        self._clock = clock
        self._failures: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def _prune(self, key: str, now: float) -> deque[float]:
        q = self._failures.setdefault(key, deque())
        while q and now - q[0] >= self.window:
            q.popleft()
        if not q:
            self._failures.pop(key, None)
        return q

    def retry_after(self, key: str) -> int:
        """Seconds until `key` may try again, or 0 if it is not blocked."""
        with self._lock:
            now = self._clock()
            q = self._prune(key, now)
            if len(q) < self.max_attempts:
                return 0
            return max(1, int(self.window - (now - q[0])) + 1)

    def record_failure(self, key: str) -> None:
        with self._lock:
            now = self._clock()
            q = self._prune(key, now)
            q.append(now)
            self._failures[key] = q

    def reset(self, key: str) -> None:
        with self._lock:
            self._failures.pop(key, None)
