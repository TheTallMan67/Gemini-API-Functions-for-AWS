import json
import gemini
import boto3
import base64
from botocore.exceptions import ClientError
from math import log10, floor
from lambda_helpers import *

ALLOWED_CURRENCIES = ["BTCUSD", "ETHUSD"]
FACTOR = 0.999

def validate_event(event, defaults={}):
    options = apply_event_defaults(event, defaults)
    print("validating options: " + json.dumps(options))
    assert "currency" in options, REQUIRED_PARAM.format("currency")
    assert options["currency"] in ALLOWED_CURRENCIES, "Unknown currency '" + options["currency"]
    assert "amount" in options, REQUIRED_PARAM.format("amount")
    assert options["amount"] > 0, "Amount ({}) must be greater than zero".format(options["amount"])
    return options

def get_tick_size(options):
    trader = gemini.PublicClient(options["sandbox"])
    currency_details = trader.symbol_details(options["currency"])
    assert type(currency_details) is dict
    assert "tick_size" in currency_details
    base10 = log10(abs(currency_details["tick_size"]))
    exponent = abs(floor(base10)) 
    return exponent

def place_buy_order(options):
    trader = get_trader(options)
    spot_price = float(trader.get_ticker(options["currency"])['ask'])
    #to set a limit order at a fixed price (ie. $55,525) set execution_price = "55525.00" or execution_price = str(55525.00)
    execution_price = str(round(spot_price * FACTOR, 2))
    # get tick size
    tick_size = get_tick_size(options)
    #set amount to the most precise rounding (tick_size) and multiply by 0.999 for fee inclusion - if you make an order for $20.00 there should be $19.98 coin bought and $0.02 (0.10% fee)
    amount = round((options["amount"] * FACTOR) / float(execution_price), tick_size)
    #execute maker buy with the appropriate symbol (options["currency"]), amount, and calculated price
    buy_order = trader.new_order(options["currency"], str(amount), execution_price, "buy", ["maker-or-cancel"])
    return buy_order

def lambda_handler(event, context):
    response = http_error("Unknown Server Error", 500)
    try:
        """
        {
            "sandbox" : false,
            "currency": "BTCUSD",
            "amount": 10
        }
        """
        # get environment from event
        print("event recieved: " + json.dumps(event))
        options = validate_event(event)
        # place buy order
        buy_order = place_buy_order(options)
        print("buy order: " + json.dumps(buy_order))
        response = http_ok(buy_order)
    except Exception as e:
        response = http_error(str(e))

    return response
