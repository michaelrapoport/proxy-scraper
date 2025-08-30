from flask import Flask, render_template
import asyncio
import time
from src.scraper import scrape_proxyscrape, scrape_spys_one, scrape_generic
from src.tester import test_proxy
from src.urls import URLS

app = Flask(__name__)

# In-memory cache
proxy_cache = []
last_cache_update = 0
CACHE_TIMEOUT = 600  # 10 minutes

# Map URLs to specific scrapers
SCRAPER_MAPPING = {
    'spys.one': scrape_spys_one,
    'proxyscrape.com': scrape_proxyscrape,
    # Add other specific scrapers here
}

SEMAPHORE_LIMIT = 10 # Limit concurrent scraping/testing tasks

async def get_working_proxies():
    """Scrapes and tests proxies from all sources with limited concurrency."""
    sem = asyncio.Semaphore(SEMAPHORE_LIMIT)

    async def scrape_with_sem(scraper, url):
        async with sem:
            return await scraper(url)

    tasks = []
    for url in URLS:
        # Find the appropriate scraper for the URL
        scraper = scrape_generic  # Default to the generic scraper
        for domain, specific_scraper in SCRAPER_MAPPING.items():
            if domain in url:
                scraper = specific_scraper
                break
        tasks.append(scrape_with_sem(scraper, url))

    scraped_proxies_lists = await asyncio.gather(*tasks, return_exceptions=True)

    # Flatten the list of lists and remove duplicates, also filter out exceptions
    all_proxies = set()
    for result in scraped_proxies_lists:
        if isinstance(result, list):
            for proxy in result:
                all_proxies.add(proxy)
        # Optionally log the exception `result` here

    # Test the proxies concurrently
    if not all_proxies:
        return []
        
    sorted_proxies = sorted(list(all_proxies))

    async def test_with_sem(proxy):
        async with sem:
            return await test_proxy(proxy)

    test_tasks = [test_with_sem(p) for p in sorted_proxies]
    test_results = await asyncio.gather(*test_tasks)

    # Filter out the proxies that failed the test
    working_proxies = [proxy for proxy, result in zip(sorted_proxies, test_results) if result]

    return working_proxies

@app.route('/')
async def index():
    global proxy_cache, last_cache_update
    current_time = time.time()

    # Check if the cache is stale
    if not proxy_cache or (current_time - last_cache_update > CACHE_TIMEOUT):
        print("Cache is stale, refreshing...")
        proxy_cache = await get_working_proxies()
        last_cache_update = current_time
    else:
        print("Serving from cache.")

    return render_template('index.html', proxies=proxy_cache)

if __name__ == '__main__':
    app.run(debug=True)
