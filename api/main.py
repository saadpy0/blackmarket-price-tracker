from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import re

from scrapers.marketplace_template import scrape_products_from_url
from utils.clean_data import clean_products
from utils.anomaly_detection import detect_anomalies_api

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str  # .onion URL

@app.post("/scrape")
def scrape_endpoint(req: ScrapeRequest):
    # Temporarily allow any http/https URL for testing
    if not re.match(r"^https?://", req.url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    try:
        # 1. Scrape products from the given URL
        products = scrape_products_from_url(req.url)
        if not products:
            return {"anomalies": [], "message": "No products found on page."}
        # 2. Clean the product data
        df = clean_products(products)
        if df.empty:
            return {"anomalies": [], "message": "No valid products after cleaning."}
        # 3. Detect anomalies
        anomalies = detect_anomalies_api(df)
        return {"anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 