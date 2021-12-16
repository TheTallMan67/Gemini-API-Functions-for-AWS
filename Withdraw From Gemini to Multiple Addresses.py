#withdraw-bitcoin lambda_function.py withdraws your available to withdraw crypto from Gemini. It takes a percentage value and as a variable to split your funds to multiple wallets. You could use this to send 10% to BlockFi and 90% to cold storage. Just remember that every withdraw you make after the first one, the percentage will calculate based on the new available withdrawal amount.
import json
import gemini

public_key = ""  
private_key = ""
trader = gemini.PrivateClient(public_key, private_key)

#withdraws full available balance of specified coin to given address
def _withdrawPartialCoinBalance(coin, address, percentage):
    amount = "0"
    for currency in trader.get_balance():
        if(currency['currency'] == coin):
            amount = currency['availableForWithdrawal'] * percentage
            print(f'Amount Available for Withdrawal: {amount}')
    
    #Replace the amount variable below with ".001" to withdraw .001 BTC - change the amount if you want to withdraw some static amount
    withdraw = trader.withdraw_to_address(coin, address, amount)

def lambda_handler(event, context):
    #Add addresses below 
    #MAKE SURE THAT YOUR WALLET ADDRESS IS FOR THE SAME TOKEN AS THE WITHDRAWAL SYMBOL OR YOU COULD LOSE FUNDS
    #(ie. in _withdrawPartialCoinBalance(bitcoin_withdrawal_symbol, btc_address, .75) both btc_address and bitcoin_withdrawal_symbol reference the same coin (BTC))

    bitcoin_withdrawal_symbol = "BTC"
    #for full list of symbols -> https://docs.gemini.com/rest-api/#symbols-and-minimums
 
    btc_address = ''
    btc_address_2 = ''

    #withdrawals 75% of your available balance
    _withdrawPartialCoinBalance(bitcoin_withdrawal_symbol, btc_address, .75)
    #withdrawals 100% of the 25% of your original remaining balance
    _withdrawPartialCoinBalance(bitcoin_withdrawal_symbol, btc_address_2, 1)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }