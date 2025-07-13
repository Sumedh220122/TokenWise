import os
from pymongo import MongoClient
from typing import List
from dotenv import load_dotenv
from database_models import TokenHolderDBModel, TransactionDBModel
from datetime import datetime

load_dotenv()

class DatabaseConnection:

    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.mongo_uri = os.getenv("MONGO_URI")

    def insert_token_holders(self, holders: List[TokenHolderDBModel]):
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db["token_holders"]

            for holder in holders:
                collection.insert_one(holder.model_dump())
        except Exception as e:
            print(f"Error inserting token holders: {e}")
            return False
        return True
    
    def insert_transactions(self, transactions: List[TransactionDBModel]):
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db["transactions"]
            for transaction in transactions:
                collection.insert_one(transaction.model_dump())
        except Exception as e:
            print(f"Error inserting transactions: {e}")
            return False
        return True
    
    def get_token_holders(self, start_date: datetime) -> List[TokenHolderDBModel]:
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db["token_holders"]
            holders = list(collection.find({"session_date": start_date}))
            return [TokenHolderDBModel(**holder) for holder in holders]
        except Exception as e:
            print(f"Error getting token holders: {e}")
            return []
        
    def get_transactions(self, start_date: datetime) -> List[TransactionDBModel]:
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db["transactions"]
            transactions = list(collection.find({"session_date": start_date}))
            return [TransactionDBModel(**transaction) for transaction in transactions]
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
        
    def get_session_dates(self) -> List[datetime]:
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db["transactions"]
            transactions = list(collection.find({}))
            # Return unique session dates as datetime objects
            return sorted(list(set(transaction["session_date"] for transaction in transactions)))
        except Exception as e:  
            print(f"Error getting session dates: {e}")
            return []