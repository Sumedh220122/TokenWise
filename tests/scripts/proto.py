import os
import json
import requests

def get_top60_holders():
    # Actual Logic
    # RPC_BASE_URL = os.getenv("HELIUS_RPC_URL")
    # API_KEY = os.getenv("HELIUS_API_KEY")
    # RPC_URL = f"{RPC_BASE_URL}/?api-key={API_KEY}"

    # payload = {
    #     "jsonrpc": "2.0",
    #     "id": "1",
    #     "method": "getTokenAccounts",
    #     "params": { "mint": "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump" }
    # }
    # headers = {"Content-Type": "application/json"}

    # response = requests.post(RPC_URL, json=payload, headers=headers)
    # data = response.json()

    # holders = data.get("result", {}).get('token_accounts', [])
    # holders = sorted(holders, key = lambda x: x["amount"], reverse = True)[:60]

    # Mocking
    with open("top60.json", "r") as f:
        holders = json.load(f)

    return holders

def get_holder_balances(holders):
    # Actual Logic
    # RPC_BASE_URL = os.getenv("HELIUS_RPC_URL")
    # API_KEY = os.getenv("HELIUS_API_KEY")
    # RPC_URL = f"{RPC_BASE_URL}/?api-key={API_KEY}"

    # holder_addrs = [holder["owner"] for holder in holders]

    # for addr in holder_addrs[0:5]:
    #     payload = {
    #         "jsonrpc": "2.0",
    #         "id": "1",
    #         "method": "getBalance",
    #         "params": [addr]
    #     }
    #     headers = {"Content-Type": "application/json"}

    #     response = requests.post(RPC_URL, json=payload, headers=headers)
    #     data = response.json()

    #     return data

    holders = get_top60_holders()
    
    with open("balances.json", "r") as f:
        balances = json.load(f)
    
    for i in range(5):
        holders[i]["balance"] = balances["balances"][i]["result"]["value"]

    return holders[0:5]

def analyze_transactions():
    holders = get_top60_holders()
    balances = get_holder_balances(holders)
    
    with open("transactions.json", "r") as f:
        data = json.load(f)

    signatures = [trans["signature"] for trans in data["result"]]

    with open("transactions_2.json", "r") as f:
        tx_data = json.load(f)

    print(len(tx_data[0]))

    for tx in tx_data:
        fromUser = tx[0]["nativeTransfers"][0]["fromUserAccount"]
        toUser = tx[0]["nativeTransfers"][0]["toUserAccount"]
        amount = tx[0]["nativeTransfers"][0]["amount"]

        blcChange = [accdata["nativeBalanceChange"] for accdata in tx[0]["accountData"] if accdata["account"] == fromUser][0]

        if blcChange < 0:
            print("Sell")
        else:
            print("Buy")

        protocol = tx[0]["source"]
        print("Protocol:", protocol)

        timestamp = tx[0]["timestamp"]
        print("timestamp")

analyze_transactions()


    
