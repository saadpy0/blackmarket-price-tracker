from utils.tor_connection import fetch_via_tor
from utils.data_storage import append_row
from datetime import datetime
from bs4 import BeautifulSoup

MARKETPLACE = 'books.toscrape.com'
URL = 'http://books.toscrape.com/catalogue/page-1.html'


def scrape_books():
    print(f"Fetching {URL} via Tor...")
    html = fetch_via_tor(URL)
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.select('article.product_pod')
    for book in books:
        title = book.h3.a['title']
        price = book.select_one('.price_color').text.strip().replace('£', '')
        data = {
            'timestamp': datetime.utcnow().isoformat(),
            'marketplace': MARKETPLACE,
            'product_name': title,
            'price': price,
            'currency': 'GBP',
            'vendor': '',
            'url': URL,
            'raw_html': str(book)
        }
        append_row(data)
        print(f"Saved: {title} - £{price}")

if __name__ == "__main__":
    scrape_books() 