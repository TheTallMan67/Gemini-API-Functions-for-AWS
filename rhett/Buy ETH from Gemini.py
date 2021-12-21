#buy-bitcoin lambda_function.py, buys $10 of ETH on execution once you provide API keys from Gemini
import json
import gemini

public_key = ""  
private_key = ""
symbol = "ETHUSD"
tick_size = 6
#update symbol based on what crypto/fiat pair you want to buy. Default is BTCUSD, change to BTCEUR for Euros or ETHUSD for Ethereum (for example) - see all possibilities down in symbols and minimums link
#update tick size based on what crypto-pair you are buying. ETH is 6. Check out the API link below to see what you need for your pair
#https://docs.gemini.com/rest-api/#symbols-and-minimums

def _buyEtherium(buy_size,pub_key, priv_key):
    # Set up a buy for the current price
    trader = gemini.PrivateClient(pub_key, priv_key)
    factor = 0.999
    price = str(round(float(trader.get_ticker(symbol)['ask'])*.999,2))

    #most precise rounding + *.999 for fee inclusion
    eth_amount = round((buy_size*factor)/float(price),tick_size)

    #execute maker buy, round to 8 decimal places for precision, multiply price by 2 so your limit order always gets fully filled
    buy = trader.new_order(symbol, str(eth_amount), price, "buy", ["maker-or-cancel"])
    print(f'Maker Buy: {buy}')

def lambda_handler(event, context):
    _buyEtherium(10, public_key, private_key)
    return {
        'statusCode': 200,
        'body': json.dumps('End of script')
    }