import threading
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
    threads = []

    for chunk in chunks:
        thread = threading.Thread(target=worker, args=(chunk,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start_time
    print(f"threading parser time = {elapsed:.4f} sec")


if __name__ == "__main__":
    main()
