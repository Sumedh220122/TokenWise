
from pydantic import BaseModel

class Transaction(BaseModel):
    TimeStamp: int | None
    Amount: int | None
    isBuy: bool | None
    Protocol: str
    WalletAddress: str