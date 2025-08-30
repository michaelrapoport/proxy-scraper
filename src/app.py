"""
A Flask web application for scraping and displaying working SOCKS5 proxies.
"""

import asyncio
import time
from collections.abc import Awaitable, Callable

from flask import Flask, render_template

from src.scraper import (
    scrape_generic,
    scrape_proxyscrape,
    scrape_spys_one,
)
from src.tester import test_proxy
from src.urls import URLS

app = Flask(__name__)

# Type alias for a scraper function
ScraperFunc = Callable[[str], Awaitable[list[str]]]

# In-memory cache
proxy_cache: list[str] = []
# pylint: disable=invalid-name
last_cache_update: float = 0
CACHE_TIMEOUT: int = 600  # 10 minutes

# Map URLs to specific scrapers
SCRAPER_MAPPING: dict[str, ScraperFunc] = {
    "spys.one": scrape_spys_one,
    "proxyscrape.com": scrape_proxyscrape,
    # Add other specific scrapers here
}

SEMAPHORE_LIMIT: int = 10  # Limit concurrent scraping/testing tasks


async def get_working_proxies() -> list[str]:
    """Scrape and test proxies from all sources with limited concurrency."""
    sem = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async def scrape_with_sem(scraper: ScraperFunc, url: str) -> list[str]:
        """Run a scraper within the concurrency limit."""
        async with sem:
            return await scraper(url)

    tasks: list[asyncio.Task[list[str]]] = []
    for url in URLS:
        scraper: ScraperFunc = scrape_generic  # Default to the generic scraper
        for domain, specific_scraper in SCRAPER_MAPPING.items():
            if domain in url:
                scraper = specific_scraper
                break
        tasks.append(asyncio.create_task(scrape_with_sem(scraper, url)))

    scraped_results: list[list[str] | BaseException] = list(
        await asyncio.gather(*tasks, return_exceptions=True)
    )

    all_proxies: set[str] = set()
    for result in scraped_results:
        if isinstance(result, list):
            all_proxies.update(result)

    if not all_proxies:
        return []

    sorted_proxies: list[str] = sorted(list(all_proxies))

    async def test_with_sem(proxy: str) -> bool:
        """Run a proxy test within the concurrency limit."""
        async with sem:
            return await test_proxy(proxy)

    test_tasks: list[asyncio.Task[bool]] = [
        asyncio.create_task(test_with_sem(p)) for p in sorted_proxies
    ]
    test_results: list[bool] = list(await asyncio.gather(*test_tasks))

    working_proxies: list[str] = [
        proxy for proxy, result in zip(sorted_proxies, test_results) if result
    ]

    return working_proxies


@app.route("/")
async def index() -> str:
    """
    Render the main page with a list of working proxies.

    Updates the cache if it's stale.
    """
    global proxy_cache, last_cache_update
    current_time = time.time()

    if not proxy_cache or (current_time - last_cache_update > CACHE_TIMEOUT):
        print("Cache is stale, refreshing...")
        proxy_cache = await get_working_proxies()
        last_cache_update = current_time
    else:
        print("Serving from cache.")

    return render_template("index.html", proxies=proxy_cache)


if __name__ == "__main__":
    app.run(debug=True)
