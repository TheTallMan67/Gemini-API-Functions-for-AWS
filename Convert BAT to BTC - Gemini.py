#Converts all your BAT (if you have any in your gemini account) to BTC. Replace BATBTC with BATETH to get ETH instead. For another cryptocurrency, replace BATBTC with BATUSD and then use the buy scripts to continue your DCA into those tokens with your extra USD from the BAT tokens. 
import json
import gemini
from math import floor

public_key = ""  
private_key = ""
symbol = 'BATBTC'
tick_size = 6
quote_currency_price_increment = 8
#update symbol based on what crypto/fiat pair you want to buy. Default is BATBTC, change to BATETH for ETH or BATUSD for USD (for example) - see all possibilities down in symbols and minimums link
#update tick size based on what crypto-pair you are buying. All BAT pairs are 6. Check out the API link below to see what you need for your pair
#update you quote_currency_price_increment based on the BAT pair you're trading. BTC is 8, ETH is 7, USD is 5
#https://docs.gemini.com/rest-api/#symbols-and-minimums


def _convertBAT(pub_key, priv_key, sell_size=0):
    bat_balance = 0
    trader = gemini.PrivateClient(pub_key, priv_key)
    if(list((type['available'] for type in  trader.get_balance() if type['currency'] == 'BAT'))):
        bat_balance = str(list((type['available'] for type in  trader.get_balance() if type['currency'] == 'BAT'))[0])
        print(f"BAT balance = {bat_balance}")
    if sell_size == 0:
        sell_size = (floor(float(bat_balance)*(10**(tick_size))))/(10**(tick_size))
        print(f"Sell size = {sell_size}")

    price = str(round(float(trader.get_ticker(symbol)['ask'])*0.999,quote_currency_price_increment))
    print(f"Price: {price}")

    #execute maker sell
    sell = trader.new_order(symbol, str(sell_size), price, "sell", ["maker-or-cancel"])
    print(f'Maker Sell: {sell}')
    return [sell_size, price]


def lambda_handler(event, context):
    #Provide optional third parameter sell size to _convertBAT to only convert a BTC sized portion of your BAT
    #ie. _convertBAT(public_key, private_key, .00001) to sell .00001 BTC of your BAT stack
    message = _convertBAT(public_key, private_key)
    return {
        'statusCode': 200,
        'body': json.dumps(f'Placed maker sell order for {symbol}.')
    }