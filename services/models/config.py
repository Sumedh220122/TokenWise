from pydantic import BaseModel

class Config(BaseModel):
    RPC_URL: str
    ENHANCED_TXFETCH_URL: str