import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import re
from typing import List

async def scrape_proxyscrape(url: str) -> List[str]:
    """Scrapes proxies from proxyscrape.com."""
    proxies = set()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()  # raise exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')
        # In proxyscrape, the proxies are in a textarea, so we need to find that
        textarea = soup.find('textarea')
        if textarea:
            for line in textarea.text.strip().split('\n'):
                proxies.add(line.strip())
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Error scraping {url}: {e}")

    return list(proxies)


async def scrape_spys_one(url: str) -> List[str]:
    """Scrapes proxies from spys.one."""
    proxies = set()
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, timeout=60000)

            # Wait for the table rows to be visible
            await page.wait_for_selector('tr.spy1x, tr.spy1xx', timeout=10000)

            rows = await page.locator('tr.spy1x, tr.spy1xx').all()

            ip_port_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}')

            for row in rows:
                first_cell_text = await row.locator('td').first.text_content()
                if first_cell_text:
                    match = ip_port_pattern.search(first_cell_text)
                    if match:
                        proxies.add(match.group(0))

            await browser.close()
    except Exception as e:
        print(f"Error scraping {url} with Playwright: {e}")

    return list(proxies)

async def scrape_generic(url: str) -> List[str]:
    """A generic scraper that looks for IP:port patterns."""
    proxies = set()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()

        # Use a regex to find all IP:port combinations
        ip_port_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}')
        found_proxies = ip_port_pattern.findall(response.text)
        for proxy in found_proxies:
            proxies.add(proxy)

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"Error scraping {url} with generic scraper: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with the generic scraper for {url}: {e}")

    return list(proxies)
