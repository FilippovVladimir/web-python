import os
import re
from datetime import datetime

import psycopg
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/time_manager",
)

TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)

app = FastAPI(title="Parser Service", version="1.0.0")


class ParseRequest(BaseModel):
    url: str = Field(min_length=5, max_length=500)


def init_db() -> None:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS parsed_pages (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    parsed_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )
        conn.commit()


def save_page(url: str, title: str) -> None:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO parsed_pages (url, title, parsed_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (url) DO UPDATE
                SET title = EXCLUDED.title, parsed_at = EXCLUDED.parsed_at
                """,
                (url, title, datetime.now()),
            )
        conn.commit()


def extract_title(html: str) -> str:
    match = TITLE_PATTERN.search(html)
    if match is None:
        return "No title"
    title = match.group(1).strip()
    return re.sub(r"\s+", " ", title)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Parser service is running"}


@app.post("/parse")
def parse(data: ParseRequest) -> dict:
    try:
        response = requests.get(data.url, timeout=15)
        response.raise_for_status()
        title = extract_title(response.text)
        save_page(data.url, title)
        return {
            "message": "Parsing completed",
            "url": data.url,
            "title": title,
        }
    except requests.RequestException as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
