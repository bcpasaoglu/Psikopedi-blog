from backend.ratelimit import FailedLoginLimiter


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_window_expires():
    clock = FakeClock()
    limiter = FailedLoginLimiter(max_attempts=2, window_seconds=60, clock=clock)
    limiter.record_failure("1.2.3.4")
    limiter.record_failure("1.2.3.4")
    assert limiter.retry_after("1.2.3.4") == 61
    assert limiter.retry_after("5.6.7.8") == 0  # other clients are unaffected
    clock.now = 59
    assert limiter.retry_after("1.2.3.4") > 0
    clock.now = 60
    assert limiter.retry_after("1.2.3.4") == 0
