import csv
import os
from datetime import datetime

CSV_FILE = 'data/market_data.csv'
FIELDNAMES = [
    'timestamp', 'marketplace', 'product_name', 'price', 'currency', 'vendor', 'url', 'raw_html'
]

def append_row(data, csv_file=CSV_FILE):
    """
    Append a row of data to the CSV file. Data should be a dict matching FIELDNAMES.
    """
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Example usage:
# append_row({
#     'timestamp': datetime.utcnow().isoformat(),
#     'marketplace': 'test_market',
#     'product_name': 'Example Product',
#     'price': 100,
#     'currency': 'USD',
#     'vendor': 'vendor123',
#     'url': 'http://example.com/product',
#     'raw_html': '<html>...</html>'
# }) 