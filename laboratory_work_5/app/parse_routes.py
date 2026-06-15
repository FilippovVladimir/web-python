import os

import httpx
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.celery_app import celery_app
from app.tasks import parse_url_task


router = APIRouter(prefix="/parse", tags=["parse"])

PARSER_URL = os.getenv("PARSER_URL", "http://localhost:8001")


class ParseRequest(BaseModel):
    url: str = Field(min_length=5, max_length=500)


@router.post("/sync")
async def parse_sync(data: ParseRequest) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PARSER_URL}/parse",
                json={"url": data.url},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/async")
async def parse_async(data: ParseRequest) -> dict:
    task = parse_url_task.delay(data.url)
    return {
        "task_id": task.id,
        "message": "Parsing started",
        "url": data.url,
    }


@router.get("/status/{task_id}")
async def parse_status(task_id: str) -> dict:
    result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": result.status,
    }
    if result.ready():
        if result.failed():
            response["error"] = str(result.result)
        else:
            response["result"] = result.result
    return response
