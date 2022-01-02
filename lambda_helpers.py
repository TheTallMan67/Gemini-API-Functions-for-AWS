import json
import gemini
import boto3

REQUIRED_PARAM = "Missing required parameter: {}"
ACCOUNT_ID = "***REMOVED***"
REGION_NAME = "***REMOVED***"
SYSTEM_DEFAULTS = {
    "sandbox" : True,
    "region" : REGION_NAME,
    "account_id" : ACCOUNT_ID
}

def apply_event_defaults(event, defaults={}):
    print("applying defaults: " + json.dumps(SYSTEM_DEFAULTS) + " " + json.dumps(defaults))
    options = {
        **SYSTEM_DEFAULTS, **defaults, **event
    }
    assert type(options) is dict
    assert "sandbox" in options, REQUIRED_PARAM.format("sandbox")
    assert "region" in options, REQUIRED_PARAM.format("region")
    assert "account_id" in options, REQUIRED_PARAM.format("account_id")
    return options

def _http_response(statusCode, data = {}):
    http_response = {
        "headers" : {
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

def http_error(err, statusCode = 400):
    return _http_response(statusCode, err)

def generate_secret_arn(options):
    if (options["sandbox"]):
        key = "***REMOVED***"
    else:
        key = "***REMOVED***"
    return "arn:aws:secretsmanager:{}:{}:secret:{}".format(options["region"], options["account_id"], key)

def get_secrets(options):
    aws_session = boto3.session.Session()
    secret_client = aws_session.client(
        service_name = 'secretsmanager',
        region_name = options["region"]
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

def get_trader(options):
    # get secrets
    secrets = get_secrets(options)
    # create trader
    return gemini.PrivateClient(secrets["public_key"], secrets["private_key"], options["sandbox"])