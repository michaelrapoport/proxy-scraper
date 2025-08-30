"""
This module defines the Flask routes for the application.
"""
import asyncio
import logging
from typing import Awaitable, Callable, Any

from flask import Blueprint, jsonify, render_template

from src import config, scraper
from src.core import fetch_and_test_proxies, ProxyProcessingError
from src.cache import cache

main = Blueprint("main", __name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@main.route("/")
def index():
    """Renders the main page."""
    return render_template("index.html")


@main.route("/proxies")
@cache.cached(timeout=600)  # Caches the results for 10 minutes.
def get_proxies():
    """
    Scrapes, tests, and geolocates SOCKS5 proxies, returning them as JSON.
    """
    logging.info("Proxy processing initiated.")

    scraping_funcs: list[Callable[[str], Awaitable[list[str]]]] = [
        scraper.scrape_proxyscrape,
        scraper.scrape_spys_one,
        scraper.scrape_generic,
    ]

    try:
        proxies: list[dict[str, Any]] = asyncio.run(
            fetch_and_test_proxies(scraping_funcs, config.PROXY_URLS)
        )
        logging.info("Successfully processed %d proxies.", len(proxies))
        return jsonify(proxies)

    except ProxyProcessingError as e:
        logging.error("Proxy processing error: %s", e)
        return jsonify({"error": "Proxy processing failed"}), 500
    except Exception as e:
        logging.error("Unexpected error during proxy processing: %s", e)
        return jsonify({"error": "Internal server error"}), 500
