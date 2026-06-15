import os
from datetime import datetime

import psycopg


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/time_manager",
)


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
