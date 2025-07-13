import requests
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
import os
from models import TokenHolder, TokenTransfer, Transaction
from database import DatabaseConnection
from database_models import TokenHolderDBModel, TransactionDBModel, TokenTransferDBModel
from datetime import datetime
import pandas as pd

load_dotenv()

class TokenWise:
    def __init__(self):
        self.api_key = os.getenv("HELIUS_API_KEY")
        self.mint_address = os.getenv("TOKEN_ADDRESS")
        self.db = DatabaseConnection()

    
    def start_session(self) -> List[Transaction]:
        """
        Starts a new session
        """
        start_date = datetime.now()
        top60_holders = self.get_top60_holders(start_date)
        all_transfers = self.get_transaction_history(top60_holders, start_date)
        return all_transfers

    def get_top60_holders(self, start_date: datetime) -> List[TokenHolder]:
        """
        Returns the top 60 holders of the token by wallet balance
        """
        response = requests.post(
            url = "https://mainnet.helius-rpc.com/?api-key=f025f850-f1a4-46bc-829c-f5be386a8bb5",
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer 1234567890"
            },
            json = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "getTokenLargestAccounts",
                "params": [self.mint_address]
            }
        )

        holders = json.loads(response.text)["result"]["value"]
        top60_holders = [TokenHolder(
            address=holder["address"], amount=float(holder["uiAmountString"])) 
            for holder in holders[:60]]
        
        for holder in top60_holders:
            top60_dbrecords = [TokenHolderDBModel(address=holder.address, amount=holder.amount, session_date=start_date)]
            self.db.insert_token_holders(top60_dbrecords)

        return top60_holders
    
    def get_transaction_history(self, holders: List[TokenHolder], start_date: datetime) -> List[Transaction]:
        """
           Returns the transaction history of the top 60 holders
        """
        all_transfers: List[Transaction] = []
        for holder in holders:
            try:
                url = f"https://api.helius.xyz/v0/addresses/{holder.address}/transactions?api-key={self.api_key}"
                response = requests.get(url)
            except Exception as e:
                print(f"Error fetching transactions for {holder.address}: {e}")
                continue

            data = response.json()

            for item in data:
                token_transfer = None
                try:
                    if len(item["tokenTransfers"]) > 0:
                        transfer = item["tokenTransfers"][0]
                        token_transfer = TokenTransfer(
                            timestamp = item["timestamp"],
                            from_address = transfer["fromUserAccount"],
                            to_address = transfer["toUserAccount"],
                            from_token_account = transfer["fromTokenAccount"],
                            to_token_account = transfer["toTokenAccount"],
                            amount = transfer["tokenAmount"],
                            mint = transfer["mint"],
                            protocol = item["source"]
                        )

                        direction = self.classify_transactions(item, holder.address)

                        all_transfers.append(Transaction(
                            holder_address=holder.address, 
                            token_transfers=token_transfer, 
                            direction=direction,
                            session_date=start_date
                        ))
                
                except Exception as e:
                    print(f"Error processing transaction for {holder.address}: {e}")
                    continue

        for transaction in all_transfers:
            token_transfer_dbrecords = TokenTransferDBModel(from_address=transaction.token_transfers.from_address, 
                                                             to_address=transaction.token_transfers.to_address, 
                                                             amount=transaction.token_transfers.amount,
                                                             timestamp=transaction.token_transfers.timestamp,
                                                             protocol=transaction.token_transfers.protocol)
            
            transaction_dbrecords = [TransactionDBModel(holder_address=transaction.holder_address, 
                                                        token_transfers=token_transfer_dbrecords, 
                                                        direction=transaction.direction,
                                                        session_date=start_date)]
            self.db.insert_transactions(transaction_dbrecords)

        return all_transfers
    
    def get_token_holders(self, start_date: datetime) -> List[TokenHolder]:
        """
        Returns the token holders from the database
        """
        holders = self.db.get_token_holders(start_date)
        return [TokenHolder(address=holder.address, amount=holder.amount) for holder in holders]
    
    def get_transactions(self, start_date: datetime) -> List[Transaction]:
        """
        Returns the transactions from the database
        """
        transactions = self.db.get_transactions(start_date)
        return [Transaction(
            holder_address=tx.holder_address,
            token_transfers=TokenTransfer(
                timestamp=tx.token_transfers.timestamp,
                from_address=tx.token_transfers.from_address,
                to_address=tx.token_transfers.to_address,
                amount=tx.token_transfers.amount,
                protocol=tx.token_transfers.protocol
            ),
            direction=tx.direction,
            session_date=tx.session_date
        ) for tx in transactions]
    
    def classify_transactions(self, data: List[Dict[str, Any]], holder_address: str) -> str:
        """
        Classifies the transaction direction based on the transaction data
        """
        event = data["events"]
        
        if event == {}:
            if data["tokenTransfers"][0]["fromUserAccount"] == holder_address:
                return "sell"
            else:
                return "sell"
            
        else:
            swap_event = event["swap"]
            for token_input in swap_event.get("tokenInputs", []):
                if token_input["userAccount"] == holder_address:
                    return "sell"

            for token_output in swap_event.get("tokenOutputs", []):
                if token_output["userAccount"] == holder_address:
                    return "buy"
        return "unknown"
    
    def get_session_dates(self) -> List[datetime]:
        """
        Returns the session dates from the database
        """
        return self.db.get_session_dates()

    def get_transaction_report(self, start_date: datetime) -> pd.DataFrame:
        """
        Generates a detailed transaction report for the given session date
        Returns a pandas DataFrame that can be exported to Excel/CSV
        """
        transactions = self.get_transactions(start_date)
        
        # Transform transactions into a list of dictionaries for the report
        report_data = []
        for tx in transactions:
            report_data.append({
                'Date': start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'Holder Address': tx.holder_address,
                'From Address': tx.token_transfers.from_address,
                'To Address': tx.token_transfers.to_address,
                'Amount': f"{tx.token_transfers.amount:,.2f}",
                'Protocol': tx.token_transfers.protocol,
                'Direction': tx.direction.upper(),
                'Timestamp': datetime.fromtimestamp(tx.token_transfers.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Create DataFrame and sort by timestamp
        df = pd.DataFrame(report_data)
        df = df.sort_values('Timestamp', ascending=False)
        
        return df

    def analyze_wallet_activity(self, start_date: datetime) -> pd.DataFrame:
        """
        Analyzes wallet activity patterns to identify frequent traders
        Returns a DataFrame with wallet activity statistics
        """
        transactions = self.get_transactions(start_date)
        
        # Track wallet activity
        wallet_stats = {}
        
        for tx in transactions:
            # Get the addresses involved
            from_addr = tx.token_transfers.from_address
            to_addr = tx.token_transfers.to_address
            
            # Initialize wallet stats if not exists
            for addr in [from_addr, to_addr]:
                if addr not in wallet_stats:
                    wallet_stats[addr] = {
                        'total_transactions': 0,
                        'sent_count': 0,
                        'received_count': 0,
                        'total_amount_sent': 0.0,
                        'total_amount_received': 0.0,
                        'protocols_used': set(),
                        'last_activity': None,
                        'first_activity': None
                    }
            
            # Update statistics
            amount = float(tx.token_transfers.amount)
            timestamp = datetime.fromtimestamp(tx.token_transfers.timestamp)
            
            # Sender stats
            wallet_stats[from_addr]['total_transactions'] += 1
            wallet_stats[from_addr]['sent_count'] += 1
            wallet_stats[from_addr]['total_amount_sent'] += amount
            wallet_stats[from_addr]['protocols_used'].add(tx.token_transfers.protocol)
            
            # Update activity timestamps for sender
            if not wallet_stats[from_addr]['first_activity'] or timestamp < wallet_stats[from_addr]['first_activity']:
                wallet_stats[from_addr]['first_activity'] = timestamp
            if not wallet_stats[from_addr]['last_activity'] or timestamp > wallet_stats[from_addr]['last_activity']:
                wallet_stats[from_addr]['last_activity'] = timestamp
            
            # Receiver stats
            wallet_stats[to_addr]['total_transactions'] += 1
            wallet_stats[to_addr]['received_count'] += 1
            wallet_stats[to_addr]['total_amount_received'] += amount
            wallet_stats[to_addr]['protocols_used'].add(tx.token_transfers.protocol)
            
            # Update activity timestamps for receiver
            if not wallet_stats[to_addr]['first_activity'] or timestamp < wallet_stats[to_addr]['first_activity']:
                wallet_stats[to_addr]['first_activity'] = timestamp
            if not wallet_stats[to_addr]['last_activity'] or timestamp > wallet_stats[to_addr]['last_activity']:
                wallet_stats[to_addr]['last_activity'] = timestamp
        
        # Convert to DataFrame
        activity_data = []
        for wallet, stats in wallet_stats.items():
            if stats['total_transactions'] > 0:  # Only include wallets with activity
                activity_period = (stats['last_activity'] - stats['first_activity']).total_seconds() / 3600 if stats['first_activity'] else 0
                activity_data.append({
                    'Wallet Address': wallet,
                    'Total Transactions': stats['total_transactions'],
                    'Sent Count': stats['sent_count'],
                    'Received Count': stats['received_count'],
                    'Total Amount Sent': f"{stats['total_amount_sent']:,.2f}",
                    'Total Amount Received': f"{stats['total_amount_received']:,.2f}",
                    'Protocols Used': ', '.join(stats['protocols_used']),
                    'First Activity': stats['first_activity'].strftime("%Y-%m-%d %H:%M:%S") if stats['first_activity'] else 'N/A',
                    'Last Activity': stats['last_activity'].strftime("%Y-%m-%d %H:%M:%S") if stats['last_activity'] else 'N/A',
                    'Activity Period (hours)': f"{activity_period:.2f}",
                    'Transaction Frequency': f"{stats['total_transactions'] / (activity_period if activity_period > 0 else 1):.2f}"
                })
        
        # Create DataFrame and sort by total transactions
        df = pd.DataFrame(activity_data)
        df = df.sort_values('Total Transactions', ascending=False)
        
        return df
