"""This module contains a function for testing and geolocating SOCKS5 proxies."""
import re
from typing import Any
import httpx


async def test_proxy(proxy: str) -> dict[str, Any] | None:
    """
    Tests a single SOCKS5 proxy. If it's working, geolocates it.
    Returns a dictionary with proxy and location info if successful, otherwise None.
    """
    # Validate proxy format before testing
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}$", proxy):
        return None

    test_urls = ["https://www.google.com", "https://www.cloudflare.com"]
    geolocation_url = "http://ip-api.com/json/"

    proxies_dict = {"all://": f"socks5://{proxy}"}

    try:
        async with httpx.AsyncClient(proxies=proxies_dict, timeout=10) as client:
            # 1. Test general connectivity
            test_success = False
            for url in test_urls:
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    test_success = True
                    break  # Exit loop on first successful connection
                except (httpx.RequestError, httpx.HTTPStatusError):
                    continue  # Try the next URL

            if not test_success:
                return None  # Proxy is not working

            # 2. Geolocate the proxy
            proxy_info: dict[str, Any] = {"proxy": proxy}
            try:
                response = await client.get(geolocation_url)
                response.raise_for_status()
                data = response.json()
                if data.get("status") == "success":
                    proxy_info.update({
                        "country": data.get("country"),
                        "city": data.get("city"),
                        "isp": data.get("isp"),
                    })
            except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
                # Geolocation failed, but the proxy works. Add placeholder data.
                proxy_info.update({
                    "country": "Unknown",
                    "city": "Unknown",
                    "isp": "Unknown",
                })

            return proxy_info

    except Exception:
        # Catch any other exception during client setup or requests
        return None
