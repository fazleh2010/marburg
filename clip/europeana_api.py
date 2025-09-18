import requests

# --- Configuration ---
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJiMTQxNGQxZS1lNzQ0LTRiOGQtYjZjMS1kZWZkNGFlZDRjYTEifQ.eyJleHAiOjE3NTE0NTA0MjYsImlhdCI6MTc1MTQ0NjgyNiwianRpIjoiNGFhNDFkNDAtZjc4Yi00M2RmLTgxMWMtMjJiNjMyNmUwZjMzIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmV1cm9wZWFuYS5ldS9hdXRoL3JlYWxtcy9ldXJvcGVhbmEiLCJhdWQiOiJodHRwczovL2F1dGguZXVyb3BlYW5hLmV1L2F1dGgvcmVhbG1zL2V1cm9wZWFuYSIsInN1YiI6ImE3OTIxMjcyLTljZTgtNGRhNS05NTU3LThkNzU0MWY5ZTkyMSIsInR5cCI6InZlcmlmeS1lbWFpbCIsImF6cCI6IlJiV1BBYXBRNiIsIm5vbmNlIjoiNGFhNDFkNDAtZjc4Yi00M2RmLTgxMWMtMjJiNjMyNmUwZjMzIiwiZW1sIjoiZWxhaGltQHN0YWZmLnVuaS1tYXJidXJnLmRlIiwiYXNpZCI6ImM2MDRjNWI2LTAzOTMtNDhkNC04MzMzLWUzNWYzYTc5YWE4YS5CRWY1aW5CV19fTS42YWRjNmNkNS03ZTliLTRjMWEtOTc1OS0wODZmZmI0ODA4YmYiLCJhc2lkIjoiYzYwNGM1YjYtMDM5My00OGQ0LTgzMzMtZTM1ZjNhNzlhYThhLkJFZjVpbkJXX19NLjZhZGM2Y2Q1LTdlOWItNGMxYS05NzU5LTA4NmZmYjQ4MDhiZiJ9.DbpmVCvCjt-UTn839ojPvg1SHZJ71cqmjHNCMIP8BkY&client_id=RbWPAapQ6&tab_id=BEf5inBW__M"  # 🔐 Replace with your actual API key
BASE_URL = "https://api.europeana.eu/record/v2/search.json"

def search_europeana(query, rows=5):
    """Search Europeana API and return the response data."""
    params = {
        "query": query,
        "rows": rows,
        "wskey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Raise error if request fails
    return response.json()

def extract_terms(data):
    """Extract and print subject terms from Europeana API results."""
    items = data.get("items", [])
    if not items:
        print("No results found.")
        return

    for item in items:
        title = item.get("title", ["[No Title]"])[0]
        subjects = item.get("dcSubject", [])
        print(f"\n📌 Title: {title}")
        print("🗂️  Subjects:", ", ".join(subjects) if subjects else "[No subjects found]")

def main():
    query = "van Gogh"
    print(f"🔍 Searching Europeana for: {query}")
    try:
        data = search_europeana(query)
        extract_terms(data)
    except requests.exceptions.RequestException as e:
        print("❌ Error while querying Europeana API:", e)

if __name__ == "__main__":
    main()
