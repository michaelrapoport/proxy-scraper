"""This module scrapes proxy IPs from multiple sources."""
import re

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import async_playwright

IP_PORT_PATTERN: re.Pattern[str] = re.compile(
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}"
)


async def scrape_proxyscrape(url: str) -> list[str]:
    """Scrapes proxies from proxyscrape.com."""
    proxies: set[str] = set()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()

        soup = BeautifulSoup(
            response.text, "lxml"
        )  # Use the faster lxml parser
        textarea = soup.find("textarea")
        if textarea:
            text = getattr(textarea, "text", "")
            if isinstance(text, str):
                for line in text.strip().split("\n"):
                    proxies.add(line.strip())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error scraping {url}: {e}")
        return []
    except httpx.RequestError as e:
        print(f"Request error scraping {url}: {e}")
        return []

    return list(proxies)


async def scrape_spys_one(url: str) -> list[str]:
    """Scrapes proxies from spys.one."""
    proxies: set[str] = set()
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, timeout=30000)

            await page.wait_for_selector(
                "tr.spy1x, tr.spy1xx", timeout=10000
            )

            rows = await page.locator("tr.spy1x, tr.spy1xx").all()

            for row in rows:
                first_cell_text = await row.locator("td").first.text_content()
                if first_cell_text:
                    match = IP_PORT_PATTERN.search(first_cell_text)
                    if match:
                        proxies.add(match.group(0))

            await browser.close()
    except PlaywrightError as e:
        print(f"Error scraping {url} with Playwright: {e}")

    return list(proxies)


async def scrape_generic(url: str) -> list[str]:
    """A generic scraper that looks for IP:port patterns."""
    proxies: set[str] = set()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()

        found_proxies: list[str] = IP_PORT_PATTERN.findall(response.text)
        for proxy in found_proxies:
            proxies.add(proxy)

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Error scraping {url} with generic scraper: {e}")

    return list(proxies)
