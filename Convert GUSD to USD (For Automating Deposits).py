#You can achieve recurring deposits from your bank account in Gemini by making a recurring purchase of GUSD. GUSD only trades in BTC/GUSD and ETH/GUSD and those markets aren't as liquid as BTC/USD or ETH/USD so it's best to convert your GUSD to USD. Which is what the above script does.
import json
import gemini

public_key = ''
private_key = ''

#This function converts all your GUSD to USD
def _convertGUSDtoUSD(pub_key, priv_key):
    gusd_balance = 0
    trader = gemini.PrivateClient(pub_key, priv_key)
    if(list((type['available'] for type in  trader.get_balance() if type['currency'] == 'GUSD'))):
        gusd_balance = str(list((type['available'] for type in  trader.get_balance() if type['currency'] == 'GUSD'))[0])
    #use "buy" to convert USD to GUSD
    #use "sell" to convert GUSD into USD
    #replace gusd_balance below to transfer a static amount, use gusd_balance to transfer all your GUSD to USD
    results = trader.wrap_order(gusd_balance, "sell")
    print(results)


def lambda_handler(event, context):
    _convertGUSDtoUSD(public_key, private_key)
    return {
        'statusCode': 200,
        'body': json.dumps('End of script')
    }