import requests
import json
import time
import os

API_URL = "https://api.myscheme.gov.in/search/v6/schemes"
API_KEY = "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc"

HEADERS = {
    "x-api-key": API_KEY,
    "origin": "https://www.myscheme.gov.in",
    "accept": "application/json"
}

def fetch_schemes(from_index=0, size=50):
    params = {
        "lang": "en",
        "q": "[]",
        "keyword": "",
        "sort": "",
        "from": from_index,
        "size": size
    }
    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
    return response.json()

def scrape_all_schemes():
    all_schemes = []
    from_index = 0
    size = 50
    total = None

    while True:
        print(f"Fetching schemes {from_index} to {from_index + size}...")
        data = fetch_schemes(from_index, size)

        if total is None:
            total = data["data"]["summary"]["total"]
            print(f"Total schemes found: {total}")

        items = data["data"]["hits"].get("items", [])
        if not items:
            break

        for item in items:
            fields = item.get("fields", {})
            all_schemes.append(fields)

        from_index += size

        if from_index >= total:
            break

        time.sleep(0.5)

    # Save raw data
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/schemes_full.json", "w", encoding="utf-8") as f:
        json.dump(all_schemes, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(all_schemes)} schemes to data/raw/schemes_full.json")
    return all_schemes

if __name__ == "__main__":
    scrape_all_schemes()