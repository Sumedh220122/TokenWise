import os
from pydantic import BaseModel
import requests
import json
from dotenv import load_dotenv
from solders.pubkey import Pubkey

load_dotenv()

mint_address_str = "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"

mint_pubkey = Pubkey.from_string(mint_address_str)

class Holder(BaseModel):
    Balance: str
    WalletAddress: str
    TokenQty: str

def getTop20Holders(mint_address: str):
    
    RPC_BASE_URL = os.getenv("HELIUS_RPC_URL")
    API_KEY = os.getenv("HELIUS_API_KEY")
    RPC_URL = f"{RPC_BASE_URL}/?api-key={API_KEY}"

    top_20_holders = None

    # try:
    #     response = requests.post(
    #         url = RPC_URL, 
    #         json ={
    #             "jsonrpc": "2.0",
    #             "id": 1,
    #             "method": "getTokenLargestAccounts",
    #             "params": [
    #                 mint_address
    #             ]
    #         })

    #     resp_json = response.json()
    #     top_20_holders = resp_json.get("result", {}).get("value", [])

    # except Exception as e:
    #     print(e)

    with open("sample_response.json", "r") as f:
        top_20_holders = json.load(f)["result"]["value"]
        
    holders_ls = []

    try:
        if top_20_holders is not None:
            for holder in top_20_holders:
                HolderObj: Holder = Holder(
                    WalletAddress = holder["address"],
                    Balance = holder["uiAmountString"],
                    TokenQty = holder["uiAmountString"]
                )

                holders_ls.append(HolderObj)
        
        print(holders_ls)
    except Exception as e:
        print(e)

getTop20Holders(mint_address_str)


