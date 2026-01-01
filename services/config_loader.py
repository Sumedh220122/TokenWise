import os
from dotenv import load_dotenv
from services.models.config import Config

load_dotenv()

def load_config() -> Config:
    """
    Function to load config from environment variables
    """
    # Load configs from env
    RPC_BASE_URL: str = os.getenv("HELIUS_RPC_URL")
    API_KEY: str = os.getenv("HELIUS_API_KEY")
    RPC_ETX_URL: str = os.getenv("HELIUS_ETX_RPC_URL") + f"api-key={API_KEY}"
    
    # Construct complete url from base url and api key
    RPC_URL: str = f"{RPC_BASE_URL}/?api-key={API_KEY}"

    config = Config(
        RPC_URL = RPC_URL,
        ENHANCED_TXFETCH_URL = RPC_ETX_URL
    )

    return config
    

    
