# Plan for SOCKS5 Proxy Scraper Webapp

This plan outlines the steps to create a web application that asynchronously crawls, scrapes, and tests SOCKS5 proxies from a list of websites.

## Phase 1: Project Setup & Core Components

- [ ] **1. Initialize Flask Application:**
    - [ ] Set up a basic Flask project structure with an `app.py`, `templates/` folder and `static/` folder.
    - [ ] Create a virtual environment and a `requirements.txt` file.

- [ ] **2. Install Dependencies:**
    - [ ] Add `Flask`, `httpx[socks]`, `beautifulsoup4`, and `playwright` to `requirements.txt`.
    - [ ] Install the dependencies using `pip install -r requirements.txt`.
    - [ ] Install Playwright browsers: `playwright install`

- [ ] **3. Create Basic Web Interface:**
    - [ ] Create a simple `index.html` in the `templates` folder to display the scraped proxies.
    - [ ] Create a Flask route in `app.py` to render the `index.html`.

## Phase 2: Scraping Engine

- [ ] **1. URL Management:**
    - [ ] Create a list of target URLs to be scraped.

- [ ] **2. Static Site Scraper:**
    - [ ] Implement a function to scrape proxies from sites with static HTML using `httpx` and `BeautifulSoup`.
    - [ ] Start with one or two simpler sites from the list (e.g., proxyscrape.com).

- [ ] **3. Dynamic Site Scraper:**
    - [ ] Implement a function to scrape proxies from sites that require JavaScript rendering using `playwright`.
    - [ ] Start with one or two dynamic sites from the list.

- [ ] **4. Asynchronous Scraping:**
    - [ ] Use `asyncio` and `httpx` to fetch multiple static URLs concurrently.
    - [ ] Use `playwright`'s async API to scrape dynamic sites concurrently.

## Phase 3: Proxy Testing

- [ ] **1. Proxy Tester Function:**
    - [ ] Create an asynchronous function that takes a proxy (IP:port) and tests its validity.
    - [ ] The test should attempt to connect to a reliable target URL (e.g., `https://www.google.com`) through the proxy using `httpx` with SOCKS5 support.
    - [ ] The function should handle timeouts and connection errors gracefully.

- [ ] **2. Asynchronous Testing:**
    - [ ] Integrate the tester function into the scraping workflow.
    - [ ] Run the tests for all scraped proxies concurrently using `asyncio`.

## Phase 4: Integration and Refinement

- [ ] **1. Main Application Logic:**
    - [ ] Create a main function that orchestrates the entire process:
        - Calls the scrapers.
        - Collects the scraped proxies.
        - Calls the testers.
        - Collects the working proxies.
    - [ ] Update the Flask route to run this main function and pass the list of working proxies to the template.

- [ ] **2. Error Handling and Logging:**
    - [ ] Implement robust error handling for network issues, parsing errors, and testing failures.
    - [ ] Add logging to monitor the scraping and testing process.

- [ ] **3. Refine Frontend:**
    - [ ] Improve the `index.html` to display the proxy list in a clear and organized table.
    - [ ] Add information like country, anonymity level if available from the source. (This might be a stretch goal).

- [ ] **4. Pagination Handling (Advanced):**
    - [ ] For each scraper, check for pagination links ("Next", page numbers, etc.).
    - [ ] If pagination is found, recursively call the scraper for each page.
