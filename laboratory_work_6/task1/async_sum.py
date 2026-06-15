import asyncio
import time

TOTAL = 10_000_000_000_000
WORKERS = 8


def calculate_sum(start: int, end: int) -> int:
    return (end - start + 1) * (start + end) // 2


async def worker(start: int, end: int) -> int:
    return await asyncio.to_thread(calculate_sum, start, end)


async def run() -> int:
    chunk_size = TOTAL // WORKERS
    tasks = []

    for i in range(WORKERS):
        chunk_start = i * chunk_size + 1
        chunk_end = (i + 1) * chunk_size if i < WORKERS - 1 else TOTAL
        tasks.append(worker(chunk_start, chunk_end))

    results = await asyncio.gather(*tasks)
    return sum(results)


def main() -> None:
    start_time = time.perf_counter()
    total = asyncio.run(run())
    elapsed = time.perf_counter() - start_time

    print("async")
    print(f"sum = {total}")
    print(f"time = {elapsed:.4f} sec")


if __name__ == "__main__":
    main()
