from pydantic import BaseModel
from typing import Optional

class TokenHolder(BaseModel):
    address: str
    amount: float

class TokenTransfer(BaseModel):
    timestamp: int
    from_address: str
    to_address: str
    from_token_account: Optional[str] = ""
    to_token_account: Optional[str] = ""
    amount: float
    mint: Optional[str] = ""
    protocol: str

class Transaction(BaseModel):
    holder_address: str
    token_transfers: TokenTransfer
    direction: str