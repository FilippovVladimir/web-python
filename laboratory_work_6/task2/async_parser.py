import asyncio
import time

import aiohttp

from db import init_db, save_page
from parser_utils import URLS, WORKERS, extract_title, split_urls


_session: aiohttp.ClientSession | None = None


async def parse_and_save(url: str) -> None:
    if _session is None:
        raise RuntimeError("Session is not initialized")
    async with _session.get(url, timeout=15) as response:
        response.raise_for_status()
        html = await response.text()
    title = extract_title(html)
    save_page(url, title)
    print(f"{url} -> {title}")


async def worker(urls: list[str]) -> None:
    for url in urls:
        await parse_and_save(url)


async def run() -> None:
    global _session
    init_db()
    chunks = split_urls(URLS, WORKERS)
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        _session = session
        await asyncio.gather(*[worker(chunk) for chunk in chunks])


def main() -> None:
    start_time = time.perf_counter()
    asyncio.run(run())
    elapsed = time.perf_counter() - start_time
    print(f"async parser time = {elapsed:.4f} sec")


if __name__ == "__main__":
    main()
