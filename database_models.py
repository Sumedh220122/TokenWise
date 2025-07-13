from pydantic import BaseModel
from datetime import datetime

class TokenHolderDBModel(BaseModel):
    session_date: datetime
    address: str
    amount: float

class TokenTransferDBModel(BaseModel):
    from_address: str
    to_address: str
    amount: float
    timestamp: int
    protocol: str

class TransactionDBModel(BaseModel):
    session_date: datetime
    holder_address: str
    token_transfers: TokenTransferDBModel
    direction: str    