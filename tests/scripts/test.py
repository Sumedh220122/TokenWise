import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RPC_BASE_URL = os.getenv("HELIUS_RPC_URL")
API_KEY = os.getenv("HELIUS_API_KEY")
RPC_URL = f"{RPC_BASE_URL}/?api-key={API_KEY}"

# payload = {
#     "jsonrpc": "2.0",
#     "id": "1",
#     "method": "getTokenAccounts",
#     "params": { "mint": "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump" }
# }


headers = {"Content-Type": "application/json"}

# response = requests.post(RPC_URL, json=payload, headers=headers)
# data = response.json()

# with open("accounts.json", "w") as f:
#     json.dump(data, f, indent = 2)

with open("accounts.json", "r") as f:
    data = json.load(f)

holders = data.get("result", {}).get('token_accounts', [])
holders = sorted(holders, key = lambda x: x["amount"], reverse = True)[:60]

with open("top60.json", "w") as f:
    json.dump(holders, f, indent = 2)


# holder_addrs = [holder["owner"] for holder in holders]

# for addr in holder_addrs[0:5]:
#     payload = {
#         "jsonrpc": "2.0",
#         "id": "1",
#         "method": "getBalance",
#         "params": [addr]
#     }

#     response = requests.post(RPC_URL, json=payload, headers=headers)
#     data = response.json()

#     print(data)
