import requests
import json
import time

API_KEY = "vouscenti"
BASE_URL = "https://api.europeana.eu/record/v2/search.json"

def extract_terms_from_item(item):
    """
    Extract relevant cultural heritage terms from a Europeana item.
    """
    terms = []
    if 'dcSubject' in item:
        terms.extend(item['dcSubject'])
    if 'concept' in item:
        terms.extend(item['concept'])
    return terms

def fetch_all_terms(api_key, max_pages=10, rows_per_page=100):
    """
    Fetch heritage items from Europeana and extract cultural terms.
    """
    all_data = []

    for page in range(max_pages):
        start = page * rows_per_page + 1
        params = {
            "wskey": api_key,
            "query": "*",
            "qf": ["YEAR:[1850 TO 1950]"],
            "rows": rows_per_page,
            "start": start,
            "profile": "rich"
        }

        print(f"[INFO] Fetching page {page + 1} (start={start})...")
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch data: HTTP {response.status_code}")
            break

        data = response.json()
        items = data.get("items", [])

        if not items:
            print("[INFO] No more items found.")
            break

        for item in items:
            terms = extract_terms_from_item(item)
            if terms:
                all_data.append({
                    "id": item.get("id"),
                    "title": item.get("title", []),
                    "terms": list(set(terms))
                })

        time.sleep(1)  # Be nice to the API

    return all_data

def save_to_json(data, filename):
    """
    Save the extracted data to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] Saved {len(data)} records to {filename}")

def main():
    print("[START] Europeana cultural heritage terms extraction.")
    if API_KEY == "YOUR_EUROPEANA_API_KEY":
        print("[ERROR] Please replace 'YOUR_EUROPEANA_API_KEY' with your actual Europeana API key.")
        return

    results = fetch_all_terms(api_key=API_KEY, max_pages=20)
    fileName="/home/melahi/code/marburg/data/europeana_heritage_terms_1850_1950.json"
    save_to_json(results,fileName)

if __name__ == "__main__":
    main()
