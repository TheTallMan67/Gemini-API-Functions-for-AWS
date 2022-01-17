# The Why

**Dollar Cost Averaging** is a technique to overcome fear in investing by mitigating the risk of loss over the short term. In other words it aims to reduce the impact of volatility on large purchases. You already do this with your index funds, so why not do it with cypto?

**Automating your invenstments** to free up your time for better things

# The How

1. Follow along with <a href="https://www.youtube.com/watch?v=h6r1h3am6kA" target="_blank">this Youtube Video</a>
2. Gather the <a href="https://rhettre.notion.site/Gemini-API-Functions-for-AWS-abe92c33a13b4be19d232d5c91edfccf" target="_blank">needed resources here</a>. 
3. Supplement the lambda functions with the ones in the repository. _Check back often for updates._

## Passing parameters to lambda functions
Instead of creating a lambda function for each different crypto (or price/coin combination) you can create a single _Event Bridge Rule_ and pass parameters to the function.
The required parameters are **sandbox**, **currency** and **amount**. Exmaple:
```
{
   "sandbox" : false, 
   "currency": "BTCUSD", 
   "amount": 10
}
```
or 
```
{
   "sandbox" : false, 
   "currency": "ETHUSD", 
   "amount": 5
}
```

# The Future
<a href="https://github.com/TheTallMan67/Gemini-API-Functions-for-AWS/discussions/new" target="_blank">Submit an Enhancement Request</a>

# <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=018" width="30" heigh="30"/> Bitcoin Accepted Here
**bc1qqyhxl0cjj885t7aqh5fmygxxclg4xketq0suaz**

<img id='btc-donations' 
            src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1qqyhxl0cjj885t7aqh5fmygxxclg4xketq0suaz" 
            alt="bc1qqyhxl0cjj885t7aqh5fmygxxclg4xketq0suaz" 
            width="150" 
            height="150"/>
