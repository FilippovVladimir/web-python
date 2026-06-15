import multiprocessing as mp
import time

from db import init_db, save_page
from parser_utils import URLS, WORKERS, extract_title, fetch_html, split_urls


def parse_and_save(url: str) -> None:
    html = fetch_html(url)
    title = extract_title(html)
    save_page(url, title)
    print(f"{url} -> {title}")


def worker(urls: list[str]) -> None:
    for url in urls:
        parse_and_save(url)


def main() -> None:
    init_db()
    chunks = split_urls(URLS, WORKERS)

    start_time = time.perf_counter()

    with mp.Pool(processes=WORKERS) as pool:
        pool.map(worker, chunks)

    elapsed = time.perf_counter() - start_time
    print(f"multiprocessing parser time = {elapsed:.4f} sec")


if __name__ == "__main__":
    main()
