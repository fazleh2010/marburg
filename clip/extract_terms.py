import requests
import time

API_KEY = 'vouscenti'
QUERY = 'painting'
BASE_URL = 'https://api.europeana.eu/record/v2/search.json'
ROWS = 100
MAX_PAGES = 5  # change this to get more data

def fetch_terms(query, rows=100, pages=5):
    terms = set()
    for page in range(pages):
        start = page * rows + 1  # Europeana sometimes dislikes start=0
        params = {
            'wskey': API_KEY,
            'query': query,
            'rows': rows,
            'start': start,
            'profile': 'rich'
        }
        print(f"Fetching records {start}–{start + rows - 1}...")
        r = requests.get(BASE_URL, params=params)
        if r.status_code != 200:
            print(f"Error {r.status_code}: {r.text}")
            break

        items = r.json().get('items', [])
        for item in items:
            for field in ['dcSubject', 'edmHasType', 'type', 'dcType']:
                if field in item:
                    terms.update(item[field])
        time.sleep(1)  # avoid rate limits
    return terms

if __name__ == '__main__':
    terms = fetch_terms(QUERY, ROWS, MAX_PAGES)
    print(f"\nFound {len(terms)} unique terms for query '{QUERY}':\n")
    for t in sorted(terms):
        print(t)
