import requests
import json
import os

def fetch_products():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        os.makedirs("data", exist_ok=True)
        with open("data/products_raw.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"Fetched {len(data)} products successfully.")
        return data
    else:
        print(f"Failed to fetch data. Status: {response.status_code}")
        return None

if __name__ == "__main__":
    fetch_products()