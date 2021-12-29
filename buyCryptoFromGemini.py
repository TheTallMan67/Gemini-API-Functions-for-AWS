import json
import gemini
import boto3
import base64
from botocore.exceptions import ClientError
from math import log10, floor

ACCOUNT_ID = "***REMOVED***"
REGION_NAME = "***REMOVED***"
REQUIRED_PARAM = "Missing required parameter: {}"
ALLOWED_CURRENCIES = ["BTCUSD", "ETHUSD"]
FACTOR = 0.999

def _httpResponse(statusCode, data = {}):
    return {
        "headers" : {
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "statusCode": statusCode,
        "body": json.dumps(data)
    }

def http_ok(data):
    return _httpResponse(200, data)

def http_error(err, statusCode = 400):
    return _httpResponse(statusCode, err)

def validate_event(event, defaults = {}):
    print("applying defaults: " + json.dumps(defaults))
    options = {
        **defaults, **event
    }
    print("validating options: " + json.dumps(options))
    assert type(options) is dict
    assert "sandbox" in options, REQUIRED_PARAM.format("sandbox")
    assert "currency" in options, REQUIRED_PARAM.format("currency")
    assert options["currency"] in ALLOWED_CURRENCIES, "Unknown currency '" + options["currency"]
    assert "amount" in options, REQUIRED_PARAM.format("amount")
    assert options["amount"] > 0, "Amount ({}) must be greater than zero".format(options["amount"])

    return options

def generate_secret_arn(options):
    if (options["sandbox"]):
        key = "***REMOVED***"
    else:
        key = "***REMOVED***"
    return "arn:aws:secretsmanager:{}:{}:secret:{}".format(REGION_NAME, ACCOUNT_ID, key)

def get_secrets(options):
    aws_session = boto3.session.Session()
    secret_client = aws_session.client(
        service_name = 'secretsmanager',
        region_name = REGION_NAME
    )
    get_secret_value_response = secret_client.get_secret_value(
        SecretId = generate_secret_arn(options)
    )
    if 'SecretString' in get_secret_value_response:
        secret = json.loads(get_secret_value_response['SecretString'])
        return {
            "private_key" : secret["API Secret"],
            "public_key" : secret["API key"]
        }
    else:
        raise Exception("SecretString not found")    

def get_tick_size(options):
    trader = gemini.PublicClient(options["sandbox"])
    currency_details = trader.symbol_details(options["currency"])
    assert type(currency_details) is dict
    assert "tick_size" in currency_details
    base10 = log10(abs(currency_details["tick_size"]))
    exponent = abs(floor(base10)) 
    return exponent

def place_buy_order(trader, options):
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
        defaults = {
            "sandbox" : True
        }
        options = validate_event(event, defaults)
        # get secrets
        secrets = get_secrets(options)
        # create trader
        trader = gemini.PrivateClient(secrets["public_key"], secrets["private_key"], options["sandbox"])
        # convert GUSD to USD?
        # place buy order
        buy_order = place_buy_order(trader, options)
        print("buy order: " + json.dumps(buy_order))
        response = http_ok(buy_order)
    except Exception as e:
        response = http_error(str(e))

    return response
