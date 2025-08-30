"""Test and geolocate SOCKS5 proxies."""
import logging
import re
from typing import Any
import httpx


async def test_proxy(proxy: str) -> dict[str, Any] | None:
    """
    Test a SOCKS5 proxy and geolocate it if working.

    Returns proxy and location info if successful, otherwise None.
    """
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}$", proxy):
        logging.warning("Invalid proxy format: %s", proxy)
        return None

    test_url = "https://www.google.com"
    geolocation_url = "http://ip-api.com/json/"
    proxies_dict = {"all://": f"socks5://{proxy}"}

    try:
        async with httpx.AsyncClient(
            proxies=proxies_dict, timeout=7
        ) as client:
            # 1. Test connectivity
            try:
                response = await client.get(test_url)
                response.raise_for_status()
                logging.info("Proxy %s is working.", proxy)
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                logging.warning(
                    "Proxy %s failed connectivity test: %s", proxy, e
                )
                return None

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
                else:
                    proxy_info.update({"country": "Geo-lookup failed"})
            except (
                httpx.RequestError,
                httpx.HTTPStatusError,
                ValueError
            ) as e:
                logging.warning(
                    "Geolocation failed for %s: %s", proxy, e
                )
                proxy_info.update({"country": "Geolocation error"})

            return proxy_info

    except Exception as e:
        logging.error("Unexpected error testing proxy %s: %s", proxy, e)
        return None
