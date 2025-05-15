import requests
import urllib3

# disable warnings for self-signed cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = "https://localhost:8000/api"

# 1) GET current favorites
resp = requests.get(f"{BASE}/favorites/", verify=False)
print("GET /favorites/ →", resp.status_code, resp.json())

# 2) PUT new favorites
payload = {"tickers": ["MSFT", "AAPL", "GOOG"]}
resp = requests.put(f"{BASE}/favorites/", json=payload, verify=False)
print("PUT /favorites/ →", resp.status_code, resp.json())

# 3) GET again to confirm
resp = requests.get(f"{BASE}/favorites/", verify=False)
print("GET /favorites/ →", resp.status_code, resp.json())
