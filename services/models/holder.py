from pydantic import BaseModel

class Holder(BaseModel):
    Balance: int
    WalletAddress: str
    TokenQty: int
    TokenAccount: str
    Mint: str

class NoHolderError(Exception):
    pass

class BalanceError(Exception):
    pass