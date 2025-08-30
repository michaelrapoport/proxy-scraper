"""
This module contains centralized configuration settings for the application.
"""

# A list of URLs to scrape for SOCKS5 proxies.
PROXY_URLS = [
    (
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5"
        "&timeout=10000&country=all"
    ),
    (
        "https://openproxylist.xyz/socks5.txt"
    ),
    (
        "https://www.proxy-list.download/api/v1/get?type=socks5"
    ),
    (
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/"
        "socks5.txt"
    ),
    (
        "https://raw.githubusercontent.com/monosans/proxy-list/main/"
        "proxies/socks5.txt"
    ),
    (
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/"
        "proxy.txt"
    ),
    (
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/"
        "socks5.txt"
    ),
    (
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/"
        "socks5.txt"
    ),
    (
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/"
        "master/socks5.txt"
    ),
    (
        "https://spys.one/en/socks-proxy-list/"
    ),
]
