import os

import httpx
from celery import shared_task


PARSER_URL = os.getenv("PARSER_URL", "http://localhost:8001")


@shared_task(name="app.tasks.parse_url_task")
def parse_url_task(url: str) -> dict:
    response = httpx.post(
        f"{PARSER_URL}/parse",
        json={"url": url},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
