"""
This module contains the core logic for fetching and testing proxies.
"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from . import tester

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


async def fetch_and_test_proxies(
    scraping_funcs: list[Callable[[str], Awaitable[list[str]]]],
    urls: list[str],
) -> list[dict[str, Any]]:
    """
    Fetches proxies from multiple URLs using the provided scraping functions
    and tests them concurrently.
    """
    scraping_tasks: list[Awaitable[list[str]]] = []
    for url in urls:
        for func in scraping_funcs:
            scraping_tasks.append(func(url))

    scraped_results = await asyncio.gather(
        *scraping_tasks, return_exceptions=True
    )

    proxies: set[str] = set()
    for result in scraped_results:
        if isinstance(result, list):
            for proxy in result:
                proxies.add(proxy)

    testing_tasks = [tester.test_proxy(proxy) for proxy in proxies]
    test_results = await asyncio.gather(
        *testing_tasks, return_exceptions=True
    )

    valid_proxies: list[dict[str, Any]] = []
    for result in test_results:
        if isinstance(result, dict):
            valid_proxies.append(result)

    return valid_proxies
