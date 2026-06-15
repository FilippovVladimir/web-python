import multiprocessing as mp
import time

TOTAL = 10_000_000_000_000
WORKERS = 8


def calculate_sum(start: int, end: int) -> int:
    return (end - start + 1) * (start + end) // 2


def worker(args: tuple[int, int]) -> int:
    start, end = args
    return calculate_sum(start, end)


def main() -> None:
    chunk_size = TOTAL // WORKERS
    chunks = []

    for i in range(WORKERS):
        chunk_start = i * chunk_size + 1
        chunk_end = (i + 1) * chunk_size if i < WORKERS - 1 else TOTAL
        chunks.append((chunk_start, chunk_end))

    start_time = time.perf_counter()

    with mp.Pool(processes=WORKERS) as pool:
        results = pool.map(worker, chunks)

    total = sum(results)
    elapsed = time.perf_counter() - start_time

    print("multiprocessing")
    print(f"sum = {total}")
    print(f"time = {elapsed:.4f} sec")


if __name__ == "__main__":
    main()
