#withdraw-bitcoin lambda_function.py withdraws all your available to withdraw BTC and ETH from Gemini. It takes a public and private API KEY + public key BTC and ETH wallet addresses as strings in the btc_addresses + eth_addresses variables
import json
import gemini

public_key = ""  
private_key = ""
trader = gemini.PrivateClient(public_key, private_key)

#withdraws full available balance of specified coin to given address
def _withdrawFullCoinBalance(coin, address):
    amount = "0"
    for currency in trader.get_balance():
        if(currency['currency'] == coin):
            amount = currency['availableForWithdrawal']
            print(f'Amount Available for Withdrawal: {amount}')
    
    #Replace the amount variable below with ".001" to withdraw .001 BTC - change the amount if you want to withdraw some static amount
    withdraw = trader.withdraw_to_address(coin, address, amount)
    print(withdraw)

def lambda_handler(event, context):
    #Add addresses below 
    #MAKE SURE THAT YOUR WALLET ADDRESS IS FOR THE SAME TOKEN AS THE WITHDRAWAL SYMBOL OR YOU COULD LOSE FUNDS
    #(ie. in _withdrawPartialCoinBalance(bitcoin_withdrawal_symbol, btc_address, .75) both btc_address and bitcoin_withdrawal_symbol reference the same coin (BTC))

    bitcoin_withdrawal_symbol = "BTC"
    ethereum_withdrawal_symbol = "ETH"
    btc_address = ''
    eth_address = ''
    _withdrawFullCoinBalance(bitcoin_withdrawal_symbol, btc_address)
    _withdrawFullCoinBalance(ethereum_withdrawal_symbol, eth_address)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }