#You can achieve recurring deposits from your bank account in Gemini by making a recurring purchase of GUSD. GUSD only trades in BTC/GUSD and ETH/GUSD and those markets aren't as liquid as BTC/USD or ETH/USD so it's best to convert your GUSD to USD. Which is what the above script does.
import json
import gemini

#sandbox doesn't work with wrap orders
#public_key = 'account-RBBtUWINpiRUQNtPdL46'
#private_key = '46iR68NMwbA7XHYRMEZw6Rc2PE9d'
public_key = "account-zC3M0NdXXc31EZx7IVJm"  
private_key = "4LV8VgPPRCXGnGHNCgwztHiSxr19"

def get_balance(current_balances, currency):
    balance = -1
    if(list((type['available'] for type in current_balances if type['currency'] == currency))):
            balance = str(list((type['available'] for type in  current_balances if type['currency'] == currency))[0])
    print(currency + ' balance: ' + str(balance))
    
def get_balance_new(current_balances, currency):
    balance = -1
    for available_balance in current_balances:
        if (available_balance["currency"] == currency):
            balance = available_balance["available"]
    print(currency + ' new balance: ' + str(balance))

#This function converts all your GUSD to USD
def _convertGUSDtoUSD(pub_key, priv_key):
    trader = gemini.PrivateClient(pub_key, priv_key)
    current_balances = trader.get_balance()
    #get_balance(current_balances, 'GUSD')
    get_balance(current_balances, 'USD')
    get_balance_new(current_balances, 'USD')
    #use "buy" to convert USD to GUSD
    #use "sell" to convert GUSD into USD
    #replace gusd_balance below to transfer a static amount, use gusd_balance to transfer all your GUSD to USD
    
    #results = trader.wrap_order('10', 'sell')
    #print(results)
    #current_balances = trader.get_balance()
    #get_balance(current_balances, 'GUSD')
    #get_balance(current_balances, 'USD')


def lambda_handler(event, context):
    _convertGUSDtoUSD(public_key, private_key)
    return {
        'statusCode': 200,
        'body': json.dumps('End of script')
    }