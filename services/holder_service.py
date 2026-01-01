import requests

from services.config_loader import load_config

from services.models.holder import Holder, BalanceError, NoHolderError

class HolderService:
    def __init__(self):
        self.url = None
    
    def init_state(self):
        config = load_config()
        self.url = config.RPC_URL

    def get_top60_holders(self, mint: str):
        """
        Function to fetch the top60 holders of a given mint using helius
        args:
            mint: str - the token mint
        returns:
            holders: list[object] - the top60 holders(by amount) that hold the given mint
        """
        
        self.init_state()

        holders = None

        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "getTokenAccounts",
                "params": { "mint": mint }
            }

            headers = {"Content-Type": "application/json"}

            response = requests.post(self.url, json = payload, headers = headers)
            data = response.json()

            holders = data.get("result", {}).get('token_accounts', [])
            holders = sorted(holders, key = lambda x: x["amount"], reverse = True)[:60]

        except Exception as e:
            print(e)

        top60Holders: list[Holder] = []
        
        if holders is None:
            raise NoHolderError("Could not find any holders that hold the given mint!!")
        
        for holder in holders:
            wallet_address = holder["owner"]
            
            try:
                balance = self.calculate_balances(wallet_addr = wallet_address)

                if balance is None:
                    raise BalanceError("Could not get the balance for the current holder, skipping")
                
                holder_obj = Holder(
                    Balance = balance,
                    WalletAddress = wallet_address,
                    TokenQty = holder["amount"],
                    TokenAccount = holder["address"],
                    Mint = mint
                )

                top60Holders.append(holder_obj)
            except BalanceError:
                continue

        return top60Holders
    
    def calculate_balances(self, wallet_addr: str) -> int:
        """
        Function to calculate the wallet balance for a given holder
        args:
            wallet_addr: str - the wallet address of the holder
        returns:
            balance: int - the wallet balance of the holder(SOL) in lamports
        """
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "getBalance",
                "params": [wallet_addr]
            }

            headers = {"Content-Type": "application/json"}

            response = requests.post(self.url, json=payload, headers=headers)
            data = response.json()

            return data.get("result", {}).get("value", None)
        except Exception as e:
            print(e)
            return None

# Testing
if __name__ == "__main__":
    holder_service = HolderService()
    top60Holders = holder_service.get_top60_holders("9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump")
    print(top60Holders)
        