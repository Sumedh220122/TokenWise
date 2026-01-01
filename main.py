from services.holder_service import HolderService
from services.transaction_service import TransactionService


holder_service = HolderService()
transaction_service = TransactionService()

holders = holder_service.get_top60_holders("9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump")
transactions = transaction_service.fetch_user_transactions(holders)

print(transactions)