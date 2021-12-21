#update-bitcoin-sheet lambda_function.py pulls in transactions to your Google Sheet (named: The Definitive Bitcoin Sheet on worksheet "BTC Buy Audit File" with credentials in file: sheets_creds.json) once you fill in your keys from Gemini
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import gemini

public_key = ""  
private_key = ""


def _addTransaction(transaction):
    #populate transaction details
    transaction_date = str(datetime.fromtimestamp(transaction['timestamp']).date())
    transaction_id = float(transaction['tid'])
    provider = "Gemini"
    quantity = float(transaction['amount'])
    btc_price = float(transaction['price'])
    fee = float(transaction['fee_amount'])
    usd_amount = quantity * btc_price + fee

    #populate with new row
    return [transaction_date, transaction_id, provider, quantity, btc_price, usd_amount, fee]
    
def _authenticateSpreadsheet():
    #Set up access to the spreadsheet
    scope = ["https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("sheets_creds.json", scope)
    client = gspread.authorize(creds)
    return client.open("The Public Definitive Bitcoin Sheet").worksheet("BTC Buy Audit File")

def populateBTC(pub_key, priv_key):
    audit_file = _authenticateSpreadsheet()
    num_rows_added = 0
    trader = gemini.PrivateClient(pub_key, private_key)
    buys = trader.get_past_trades("BTCUSD")[::-1]
    last_gemini_transaction = (list(filter(lambda gemini: gemini['Provider'] == 'Gemini', audit_file.get_all_records()[-50:]))[-1]['Transaction ID'])
    for buy in buys:
        if(buy['tid'] > last_gemini_transaction):
            audit_file.append_row(_addTransaction(buy), value_input_option="USER_ENTERED")
            num_rows_added += 1
    return num_rows_added
    
def lambda_handler(event, context):
    num = populateBTC(public_key, private_key)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(f'{num} transactions added!')
    }