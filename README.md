Application flow:
1. Given a token mint address, get the top 60 holders. Store the wallet address, balance, and the token quantity
2. For these holders, analyze real time transactions
   - First, get transaction signatures ->  Done using the getSignaturesForAddresses API
   - Get the transaction details -> Done using enhanced getTransaction API
   - Track Buy/Sell. Can be done by observing the nativeBalanceChange for accounts involved in the transaction
     The from and to accounts are obtained from the nativeTransfers array from the object obtained in step 2
     Balance changes for these accounts can be observed to classify the tx as buy/sell
   - Protocol can be obtained from the source
   - Timestamps are also present in the object itself
   - 