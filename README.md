# TokenWise
A real-time intelligence tool designed to monitor and analyze wallet behavior for specific tokens on the Solana blockchain.

A real-time analytics dashboard for tracking Solana token holders and transactions. This application provides insights into token holder distributions, transaction patterns, and protocol usage.

## Features

- **Real-time Token Analytics**
  - Track top 60 token holders
  - Monitor transaction patterns
  - Analyze protocol distribution
  - View buy/sell trends

- **Session-based Analysis**
  - Start new analysis sessions
  - View historical session data
  - Compare data across different timeframes

- **Data Export Options**
  - Download token holder lists (CSV)
  - Export transaction reports (Excel/CSV)
  - Detailed transaction history

## Prerequisites

- Python 3.9 or higher
- MongoDB database

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
HELIUS_API_KEY= Your helius api key
HELIUS_RPC_URL= Your base url for helius apis
HELIUS_ETX_RPC_URL= Your base url for helius enhanced transactions api
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sumedh220122/TokenWise.git
   cd TokenWise
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Unix/MacOS
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Data Structure

- **Token Holders**
  - Wallet address
  - Wallet balance
  - Token quantity
  - Mint address
  - Token address

- **Transactions**
  - Timestamp
  - From/To addresses
  - Amount
  - Protocol
  - Direction (Buy/Sell)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
