from utils.tor_connection import fetch_via_tor
from datetime import datetime
from bs4 import BeautifulSoup

MARKETPLACE = 'books.toscrape.com'
BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'


def scrape_products_from_url(url):
    """
    Fetch the given URL via Tor, parse product data, and return a list of product dicts.
    """
    html = fetch_via_tor(url)
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.select('article.product_pod')
    products = []
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
            'url': url,
            'raw_html': str(book)
        }
        products.append(data)
    return products


def scrape_books():
    page = 1
    while True:
        url = BASE_URL.format(page)
        print(f"Fetching {url} via Tor...")
        try:
            html = fetch_via_tor(url)
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            break
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.select('article.product_pod')
        if not books:
            print(f"No products found on page {page}. Stopping.")
            break
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
                'url': url,
                'raw_html': str(book)
            }
            from utils.data_storage import append_row
            append_row(data)
            print(f"Saved: {title} - £{price}")
        page += 1

if __name__ == "__main__":
    scrape_books() 