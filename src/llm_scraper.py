"""
This module contains the agentic, LLM-driven proxy scraping logic.
"""
import logging
import re
from typing import Set

from bs4 import BeautifulSoup
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import async_playwright

IP_PORT_PATTERN: re.Pattern[str] = re.compile(
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}"
)


async def agent_scraper(url: str) -> list[str]:
    """
    An "agentic" scraper that uses a series of heuristics to find proxies
    on a webpage, handling both static and dynamic content.
    """
    logging.info("Attempting to scrape with agent: %s", url)
    proxies: Set[str] = set()

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(
                url, timeout=30000, wait_until="domcontentloaded"
            )
            await page.wait_for_timeout(5000)  # Increased wait time

            html_content = await page.content()
            await browser.close()

        soup = BeautifulSoup(html_content, "lxml")

        # Heuristics are now more robust
        text_areas = soup.find_all("textarea")
        if text_areas:
            for textarea in text_areas:
                proxies.update(IP_PORT_PATTERN.findall(textarea.get_text()))
            logging.info(
                "Found %d proxies in <textarea> for %s", len(proxies), url
            )
            return list(proxies)

        tables = soup.find_all("table")
        if tables:
            for table in tables:
                for row in table.find_all("tr"):
                    row_text = row.get_text(separator=":")
                    proxies.update(IP_PORT_PATTERN.findall(row_text))
            logging.info(
                "Found %d proxies in <table> for %s", len(proxies), url
            )
            return list(proxies)

        # Fallback to the entire body
        body_text = soup.body.get_text(separator=" ")
        proxies.update(IP_PORT_PATTERN.findall(body_text))
        logging.info("Found %d proxies in <body> for %s", len(proxies), url)

    except PlaywrightError as e:
        logging.error("Playwright error scraping %s: %s", url, e)
    except Exception as e:
        logging.error("Unexpected error scraping %s: %s", url, e)

    return list(proxies)
