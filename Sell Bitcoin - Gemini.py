#sell-bitcoin lambda_function.py, sells $20 of Bitcoin on execution once you provide API keys from Gemini - BUT FR HOMIE WHY THE HECK WOULD YOU SELL ME AND ELON MUSK YOUR PRECIOUS BITCOIN?! 
import json
import gemini

public_key = ""  
private_key = ""
symbol = 'BTCUSD'

tick_size = 8
#update symbol based on what crypto/fiat pair you want to buy. Default is BTCUSD, change to BTCEUR for Euros or ETHUSD for Ethereum (for example) - see all possibilities down in symbols and minimums link
#update tick size based on what crypto-pair you are buying. BTC is 8. Check out the API link below to see what you need for your pair
#https://docs.gemini.com/rest-api/#symbols-and-minimums

def _sellBitcoin(sell_size,pub_key, priv_key):
    # Set up a sell for 1.001X above the current price
    # Higher factor makes the order price higher but fills slower (2 would set an order for double the price and so your order could take months/years/never to fill)
    trader = gemini.PrivateClient(pub_key, priv_key)
    symbol_spot_price = float(trader.get_ticker(symbol)['ask'])
    factor = 1.001
    #to set a limit order at a fixed price (ie. $55,525) set execution_price = "55525.00" or execution_price = str(55525.00)
    execution_price = str(round(symbol_spot_price*factor,2))

    #most precise rounding + *.999 for fee inclusion
    amount = round((sell_size*.999)/float(price),tick_size)

    #execute maker sell, round to 8 decimal places for precision, multiply price by 2 so your limit order always gets fully filled
    sell = trader.new_order(symbol, str(amount), price, "sell", ["maker-or-cancel"])
    print(f'Maker Sell: {sell}')
    return [btc_amount, price]

def lambda_handler(event, context):
    message = _sellBitcoin(20, public_key, private_key)
    return {
        'statusCode': 200,
        'body': json.dumps(f'You sold {message[0]} Bitcoin for {message[1]}. You monster.')
    }