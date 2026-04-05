# 🌐 Proxy Scraper
### High-Performance Network Intelligence & Proxy Discovery

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)

**Automated proxy discovery, validation, and rotation system for resilient network operations.**

## 🚀 Overview
**Proxy Scraper** is a lightweight yet powerful tool designed to maintain a fresh, validated pool of proxies. It automatically crawls public sources, tests them for latency and anonymity, and provides a clean API for downstream applications to consume reliable proxy addresses. This is an essential component for distributed scraping, data gathering, and network research projects that require high resilience.

## ✨ Key Features
- **Automated Discovery**: Scans dozens of verified proxy lists and forums.
- **Real-time Validation**: Tests proxies against multiple target endpoints to ensure reliability.
- **Anonymity Scoring**: Categorizes proxies based on their transparency (Transparent, Anonymous, Elite).
- **Easy API**: Built on Flask to provide a simple JSON endpoint for your rotation logic.
- **Persistence**: Maintains a history of proxy performance to optimize future selection.

## 🛠️ Tech Stack
- **Backend**: Python 3.9+ / Flask
- **Concurrency**: `asyncio` / `aiohttp` for high-speed testing
- **Storage**: SQLite (configurable for Redis/PostgreSQL)

## 🎮 Getting Started

### Installation
1.  **Clone & Install**:
    ```bash
    git clone https://github.com/michaelrapoport/proxy-scraper.git
    cd proxy-scraper
    pip install -r requirements.txt
    ```
2.  **Run Service**:
    ```bash
    python app.py
    ```
3.  **Access API**:
    GET `http://localhost:5000/proxies` to get the latest validated list.

---
**Author**: M. Keith Rapoport
**License**: MIT