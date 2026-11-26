"""Small concurrent load test against a running server.

Usage: python scripts/load_test.py http://127.0.0.1:8000 --concurrency 100 --requests 2000

Exits non-zero if any request fails, so CI catches regressions such as the
connection pool deadlock this was written for.
"""

import argparse
import asyncio
import sys
import time

import httpx

PATHS = ["/api/articles", "/api/articles/stresle-basa-cikmanin-yollari", "/api/categories"]


async def run(base: str, concurrency: int, total: int) -> int:
    latencies: list[float] = []
    errors = 0
    sem = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(max_connections=concurrency)
    async with httpx.AsyncClient(base_url=base, limits=limits, timeout=15, trust_env=False) as client:

        async def one(i: int) -> None:
            nonlocal errors
            async with sem:
                start = time.perf_counter()
                try:
                    (await client.get(PATHS[i % len(PATHS)])).raise_for_status()
                except httpx.HTTPError:
                    errors += 1
                latencies.append(time.perf_counter() - start)

        started = time.perf_counter()
        await asyncio.gather(*(one(i) for i in range(total)))
        elapsed = time.perf_counter() - started

    latencies.sort()
    p50 = latencies[len(latencies) // 2] * 1000
    p95 = latencies[int(len(latencies) * 0.95)] * 1000
    print(
        f"concurrency={concurrency} requests={total} rps={total / elapsed:.0f} p50={p50:.0f}ms p95={p95:.0f}ms errors={errors}"
    )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--concurrency", type=int, default=100)
    parser.add_argument("--requests", type=int, default=2000)
    args = parser.parse_args()
    errors = asyncio.run(run(args.base_url, args.concurrency, args.requests))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
