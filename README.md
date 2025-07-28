# Black Market Price Tracker

A backend system for tracking illegal price fluctuations on dark web marketplaces for cybersecurity research. This project uses web scraping, anomaly detection, and time-series forecasting to analyze price trends and detect suspicious activity on hidden marketplaces.

## Features
- **Web Scraping via Tor**: Extracts product and price data from .onion (darknet) marketplaces using the Tor network for anonymity.
- **Data Cleaning**: Cleans and normalizes scraped data for analysis.
- **Anomaly Detection**: Identifies price anomalies using a hybrid Median Absolute Deviation (MAD) and sudden jump detection approach.
- **Time-Series Forecasting**: (Optional, for research) Uses Prophet to forecast price trends.
- **REST API**: Exposes a `/scrape` endpoint via FastAPI for programmatic access.

## Setup

### 1. Clone the Repository
```sh
git clone https://github.com/saadpy0/blackmarket-price-tracker.git
cd blackmarket-price-tracker
```

### 2. Python Environment
- Use Python 3.12.x (recommended; see [pyenv](https://github.com/pyenv/pyenv) for version management).
- Create and activate a virtual environment:
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Tor Setup
- **Tor must be installed and running as a SOCKS5 proxy on port 9050.**
- On macOS (with Homebrew):
  ```sh
  brew install tor
  brew services start tor
  ```
- Confirm Tor is running:
  ```sh
  lsof -i :9050
  ```

## Usage

### Start the API Server
```sh
source venv/bin/activate
python -m uvicorn api.main:app --reload
```

### API Endpoint
#### `POST /scrape`
- **Request Body:**
  ```json
  { "url": "http://examplemarket.onion/" }
  ```
- **Response:**
  - On success:
    ```json
    {
      "anomalies": [
        {
          "timestamp": "2024-07-28T10:00:00Z",
          "product_name": "Product X",
          "price": 123.45,
          "mad_anomaly": true,
          "jump_anomaly": false,
          "marketplace": "examplemarket.onion",
          "vendor": "",
          "url": "http://examplemarket.onion/"
        },
        ...
      ]
    }
    ```
  - If no products or anomalies are found:
    ```json
    { "anomalies": [], "message": "No products found on page." }
    ```
  - On error:
    ```json
    { "detail": "Error message" }
    ```

### Notes
- The scraper is currently tailored for sites with a structure similar to `books.toscrape.com`. For other marketplaces, the scraping logic may need to be adapted.
- Only .onion sites accessible via Tor will work reliably. Many clearnet sites block Tor exit nodes.

## Troubleshooting
- **Tor connection errors:**
  - Ensure Tor is running and listening on port 9050.
  - Test with: `curl --socks5-hostname 127.0.0.1:9050 http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/`
- **CORS errors:**
  - The API is configured to allow requests from `http://127.0.0.1:8080` for local development.
- **Module import errors:**
  - Always run scripts from the project root using the `-m` flag (e.g., `python -m scrapers.basic_scraper`).

## .gitignore
- The repository is configured to **never track data files or virtual environments**:
  - `venv/` and `data/*.csv` are excluded by default.

## License
MIT License 