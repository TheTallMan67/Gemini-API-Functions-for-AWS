#Takes authenticated client object [trader] and string crypto (ie. 'BTC', 'ETH', 'GUSD')
#Returns current balance of that crypto 
def _getCryptoBalance(trader, crypto):
    if(list((type['available'] for type in  trader.get_balance() if type['currency'] == crypto))):
        return str(list((type['available'] for type in  trader.get_balance() if type['currency'] == crypto))[0])
    return f'No balance found for: {crypto}'