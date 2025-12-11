import aiohttp

DEEZER_API_URL = "https://api.deezer.com/search"

async def search_song(query: str, limit: int = 3):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DEEZER_API_URL, params={"q": query, "limit": limit}) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception:
        return None
    return data.get("data", [])