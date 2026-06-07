import httpx
from config import settings

PEXELS_API_URL = "https://api.pexels.com/v1/search"

async def get_image_for_word(word: str) -> str | None:
    if not settings.PEXELS_API_KEY:
        return None

    headers = {"Authorization": settings.PEXELS_API_KEY}
    params = {"query": word, "per_page": 1}

    async with httpx.AsyncClient() as client:
        response = await client.get(PEXELS_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("photos") and len(data["photos"]) > 0:
                # Return the medium sized image URL
                return data["photos"][0]["src"]["medium"]
    return None
