import httpx
from app.config import OPENAI_API_KEY, OPENAI_API_URL

async def forward_to_openai(payload: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(OPENAI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
