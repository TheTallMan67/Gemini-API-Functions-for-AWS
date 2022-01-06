import json
import gemini
import boto3
import base64
from lambda_helpers import *

USD_INTO_GUSD = "buy"
GUSD_INTO_USD = "sell"

def get_balance(current_balances, currency):
    balance = -1
    for available_balance in current_balances:
        if (available_balance["currency"] == currency):
            balance = available_balance["available"]
    print(currency + ' balance: ' + str(balance))
    return balance

def convert_gusd_to_usd(options):
    trader = get_trader(options)
    
    current_balances = trader.get_balance()
    gusd_balance = get_balance(current_balances, 'GUSD')
    usd_balance = get_balance(current_balances, 'USD')

    if (options["sandbox"] == False):
        if (float(gusd_balance) > 0):
            wrap_order = trader.wrap_order("GUSDUSD", gusd_balance, GUSD_INTO_USD)
        else:
            wrap_order = {"status" : "no gusd balance"}
    else:
        wrap_order = {"status" : "not suppored on sandbox"}

    current_balances = trader.get_balance()
    gusd_balance = get_balance(current_balances, 'GUSD')
    usd_balance = get_balance(current_balances, 'USD')
    return {
        "usd_balance" : usd_balance,
        "wrap_order" : wrap_order
    }

def validate_event(event, defaults={}):
    options = apply_event_defaults(event, defaults)
    return options

def lambda_handler(event, context):
    response = http_error("Unknown Server Error", 500)
    try:
        """
        {
            "sandbox" : false
        }
        """
        # get environment from event
        print("event recieved: " + json.dumps(event))
        options = validate_event(event)
        # convert GUSD to USD
        conversion_results = convert_gusd_to_usd(options)
        print("conversion_results: " + json.dumps(conversion_results))
        response = http_ok(conversion_results)
    except Exception as e:
        response = http_error(str(e))

    return response
