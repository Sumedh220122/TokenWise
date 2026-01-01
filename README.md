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
HELIUS_API_KEY=your_helius_api_key
TOKEN_ADDRESS=your_token_mint_address
MONGO_URI=your_mongodb_connection_string
DB_NAME=your_database_name
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
   
## Running the Application

1. Ensure MongoDB is running and accessible

2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## Using the Dashboard

1. **Start a New Session**
   - Click "Start New Session" to fetch current token holder data
   - This will analyze the top 60 holders and their recent transactions

2. **View Historical Data**
   - Use the session date dropdown to select previous analysis sessions
   - Compare holder and transaction patterns across different times

3. **Export Data**
   - Use the download buttons to export data in CSV or Excel format
   - Transaction reports include detailed information about each transfer

## Data Structure

- **Token Holders**
  - Wallet address
  - Token amount
  - Rank

- **Transactions**
  - Timestamp
  - From/To addresses
  - Amount
  - Protocol
  - Direction (Buy/Sell)

## Troubleshooting

1. **MongoDB Connection Issues**
   - Verify MongoDB is running
   - Check connection string in .env file
   - Ensure network connectivity

2. **API Rate Limits**
   - Check Helius API key status
   - Monitor API usage in Helius dashboard

3. **Missing Data**
   - Verify token address is correct
   - Check if token has sufficient on-chain activity
   - Ensure all environment variables are set

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
