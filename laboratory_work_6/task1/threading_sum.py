import threading
import time

TOTAL = 10_000_000_000_000
WORKERS = 8


def calculate_sum(start: int, end: int) -> int:
    return (end - start + 1) * (start + end) // 2


def worker(start: int, end: int, results: list[int], index: int) -> None:
    results[index] = calculate_sum(start, end)


def main() -> None:
    chunk_size = TOTAL // WORKERS
    results = [0] * WORKERS
    threads = []

    start_time = time.perf_counter()

    for i in range(WORKERS):
        chunk_start = i * chunk_size + 1
        chunk_end = (i + 1) * chunk_size if i < WORKERS - 1 else TOTAL
        thread = threading.Thread(
            target=worker,
            args=(chunk_start, chunk_end, results, i),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
    elapsed = time.perf_counter() - start_time

    print("threading")
    print(f"sum = {total}")
    print(f"time = {elapsed:.4f} sec")


if __name__ == "__main__":
    main()
