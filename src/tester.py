import httpx
import asyncio

async def test_proxy(proxy):
    """Tests a single SOCKS5 proxy."""
    test_url = 'https://www.google.com'
    try:
        # The proxy needs to be in the format socks5://user:pass@host:port
        # For now, we assume no authentication is needed.
        async with httpx.AsyncClient(proxies=f"socks5://{proxy}") as client:
            response = await client.get(test_url, timeout=10)
            response.raise_for_status()
            return True
    except (httpx.RequestError, httpx.HTTPStatusError):
        return False
    except Exception:
        return False
