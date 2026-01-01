import requests

# url = "https://mainnet.helius-rpc.com/?api-key=f025f850-f1a4-46bc-829c-f5be386a8bb5"
url = "https://api-mainnet.helius-rpc.com/v0/transactions?api-key=f025f850-f1a4-46bc-829c-f5be386a8bb5"

# payload = {
#     "jsonrpc": "2.0",
#     "id": "1",
#     "method": "getSignaturesForAddress",
#     "params": ["22Wnk8PwyWZV7BfkZGJEKT9jGGdtvu7xY6EXeRh7zkBa", {"limit": 5}]
# }
# headers = {"Content-Type": "application/json"}

# response = requests.post(url, json=payload, headers=headers)

# with open("transactions.json", "w") as f:
#     import json
#     json.dump(response.json(), f, indent = 2)

with open("transactions.json", "r") as f:
    import json
    data = json.load(f)

signatures = [trans["signature"] for trans in data["result"]]

from concurrent.futures import ThreadPoolExecutor
import requests

def fetch_tx2(sig):
    payload = { "transactions": [sig] }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    return response.json()

def fetch_tx(sig):
    return requests.post(url, json={
        "jsonrpc": "2.0",
        "id": sig,
        "method": "getTransaction",
        "params": [sig, {"encoding": "jsonParsed"}]
    }).json()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_tx2, signatures[:5]))

with open("transactions_2.json", "w") as f:
    json.dump(results, f, indent = 2)
