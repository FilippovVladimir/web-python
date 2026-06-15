import re

import requests


TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://docs.python.org/3/",
    "https://www.w3.org/",
    "https://github.com",
    "https://pypi.org",
    "https://fastapi.tiangolo.com",
    "https://www.djangoproject.com",
]

WORKERS = 4


def split_urls(urls: list[str], parts: int) -> list[list[str]]:
    chunks: list[list[str]] = [[] for _ in range(parts)]
    for index, url in enumerate(urls):
        chunks[index % parts].append(url)
    return [chunk for chunk in chunks if chunk]


def extract_title(html: str) -> str:
    match = TITLE_PATTERN.search(html)
    if match is None:
        return "No title"
    title = match.group(1).strip()
    title = re.sub(r"\s+", " ", title)
    return title


def fetch_html(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text
