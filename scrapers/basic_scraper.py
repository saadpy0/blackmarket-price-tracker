from utils.tor_connection import fetch_via_tor
import json


def main():
    url = 'http://httpbin.org/ip'
    print(f"Fetching {url} via Tor...")
    response_text = fetch_via_tor(url)
    try:
        data = json.loads(response_text)
        print("IP as seen by httpbin:", data.get('origin'))
    except Exception as e:
        print("Failed to parse response:", e)
        print(response_text)

if __name__ == "__main__":
    main() 