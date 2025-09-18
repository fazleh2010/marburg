import requests
import json

# SPARQL endpoint
SPARQL_ENDPOINT = "https://sparql.europeana.eu/"

# SPARQL query to extract distinct cultural heritage terms (subjects/concepts)
SPARQL_QUERY = """
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX edm: <http://www.europeana.eu/schemas/edm/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?termLabel
WHERE {
  ?item dc:subject ?subject .
  OPTIONAL {
    ?subject skos:prefLabel ?termLabel .
    FILTER (lang(?termLabel) = "en")
  }
}
"""

# Headers for the request
HEADERS = {
    "Accept": "application/sparql-results+json"
}

# Function to run the SPARQL query
def query_europeana_sparql(query, endpoint=SPARQL_ENDPOINT):
    response = requests.get(endpoint, params={'query': query}, headers=HEADERS)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch data. Status: {response.status_code}")
        print(response.text)
        return []
    results = response.json().get("results", {}).get("bindings", [])
    return [r["termLabel"]["value"] for r in results if "termLabel" in r]

# Save results and count to JSON file
def save_with_count(data, filename):
    payload = {
        "count": len(data),
        "terms": sorted(data)
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Saved {payload['count']} terms to {filename}")

# Main script
def main():
    filename = "/home/melahi/code/marburg/data/europeana_heritage_terms.json"
    print("[START] Querying Europeana SPARQL endpoint for cultural heritage terms...")
    terms = query_europeana_sparql(SPARQL_QUERY)
    if terms:
        save_with_count(terms, filename)
    else:
        print("[INFO] No terms found.")

if __name__ == "__main__":
    main()
