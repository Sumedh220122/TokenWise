import requests
from concurrent.futures import ThreadPoolExecutor

from services.config_loader import load_config

from services.models.holder import Holder
from services.models.transaction import Transaction

class TransactionService:

    def __init__(self):
        self.config = load_config()
        self.enhanced_tx_url = self.config.ENHANCED_TXFETCH_URL
        self.url = self.config.RPC_URL

    def get_signatures(self, account_address: str):
        """
        Docstring for get_signatures
        """
        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "getSignaturesForAddress",
            "params": [account_address, {"limit": 1}]
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(self.url, json=payload, headers=headers)
        data = response.json().get("result", [])

        signatures = [obj.get("signature", "") for obj in data]

        return signatures
    
    def get_transaction_details(self, signature: str):
        payload = { "transactions": [signature] }
        headers = {"Content-Type": "application/json"}

        response = requests.post(self.enhanced_tx_url, json=payload, headers=headers)

        return response.json()
    
    def fetch_user_transactions(self, holders: list[Holder]):
        """
        Docstring for fetch_user_transactions
        
        :param self: Description
        :param holders: Description
        :type holders: list[Holder]
        """

        transactions: list[Transaction] = []

        for holder in holders:
            tokenacct_address = holder.TokenAccount

            signatures = self.get_signatures(account_address = tokenacct_address)

            with ThreadPoolExecutor(max_workers=5) as executor:
                results = list(executor.map(self.get_transaction_details, signatures))

            for result in results:
                tx_data = result[0]

                transfer_data = [acc for acc in tx_data.get("tokenTransfers", []) 
                                    if acc.get("totokenAccount", "") == tokenacct_address]

                transfer_data = transfer_data[0] if transfer_data != [] else {}

                timestamp = None
                amount = None
                is_buy = None
                protocol = None
                wallet_address = None
                
                if transfer_data != {}:
                    timestamp = tx_data.get("timestamp", None)
                    amount = transfer_data.get("tokenAmount", None)
                    is_buy = True
                    protocol = tx_data.get("source", None)
                    wallet_address = holder.WalletAddress
                else:
                    transfer_data = [acc for acc in tx_data.get("tokenTransfers", []) 
                                    if acc.get("fromtokenAccount", "") == tokenacct_address]

                    transfer_data = transfer_data[0] if transfer_data != [] else {}
                    
                    timestamp = tx_data.get("timestamp", None)
                    amount = transfer_data.get("tokenAmount", None)
                    is_buy = False
                    protocol = tx_data.get("source", "")
                    wallet_address = holder.WalletAddress
                
                transactions.append(
                    Transaction(
                        TimeStamp = timestamp,
                        Amount = amount,
                        isBuy = is_buy,
                        Protocol = protocol,
                        WalletAddress = wallet_address
                    )
                )
        
        return transactions
            
