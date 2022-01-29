import json
import gemini
import boto3

'''
# ORDER_FILL_FACTOR can be moved up/down to change the limit price of your order
(ie. 0.9 is 90% of spot price - slower fill but better price. 0.99 is 99% of
spot price - faster fill but worse price)
'''
ORDER_FILL_FACTOR = 0.999

REQUIRED_PARAM = "Missing required parameter: {}"
SYSTEM_DEFAULTS = {
    "sandbox": True,
    "orderFillFactor": ORDER_FILL_FACTOR
}


def apply_event_defaults(event, defaults={}):
    print("applying defaults: " + json.dumps(SYSTEM_DEFAULTS) + " " + json.dumps(defaults))
    options = {
        **SYSTEM_DEFAULTS, **defaults, **event
    }
    assert type(options) is dict
    assert "sandbox" in options, REQUIRED_PARAM.format("sandbox")
    assert "orderFillFactor" in options, REQUIRED_PARAM.format("orderFillFactor")
    return options


def _http_response(statusCode, data={}):
    http_response = {
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "statusCode": statusCode,
        "body": json.dumps(data)
    }
    print("HTTP Response: " + json.dumps(http_response))
    return http_response


def http_ok(data):
    return _http_response(200, data)


def http_error(err, statusCode=400):
    return _http_response(statusCode, err)


def get_secret_key(options):
    if (options["sandbox"]):
        return "GeminiAPISandbox"
    else:
        return "GeminiAPI"


def get_secrets(options):
    aws_session = boto3.session.Session()
    secret_client = aws_session.client(
        service_name='secretsmanager'
    )
    get_secret_value_response = secret_client.get_secret_value(
        SecretId=get_secret_key(options)
    )
    if 'SecretString' in get_secret_value_response:
        secret = json.loads(get_secret_value_response['SecretString'])
        return {
            "private_key": secret["API Secret"],
            "public_key": secret["API key"]
        }
    else:
        raise Exception("SecretString not found")


def get_trader(options):
    # get secrets
    secrets = get_secrets(options)
    # create trader
    return gemini.PrivateClient(secrets["public_key"], secrets["private_key"], options["sandbox"])
