import requests

def fetch_via_tor(url, timeout=30):
    """
    Fetch a web page via the Tor network using the system Tor SOCKS5 proxy.
    Returns the response text.
    """
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
    }
    response = requests.get(url, proxies=proxies, timeout=timeout)
    response.raise_for_status()
    return response.text

# Example usage (uncomment to test):
# html = fetch_via_tor('http://httpbin.org/ip')
# print(html) 