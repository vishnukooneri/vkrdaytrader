import json
import urllib.request

def handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    symbol = query_params.get('ticker', 'AAPL')
    
    # Direct connection to Yahoo Finance (No yfinance needed!)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            meta = data['chart']['result'][0]['meta']
            price = meta.get('regularMarketPrice', 0)
            prev_close = meta.get('previousClose', 0)
            change = price - prev_close
            change_pct = (change / prev_close) * 100 if prev_close else 0
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "symbol": symbol,
                    "name": meta.get('symbol', symbol),
                    "price": price,
                    "change": round(change, 2),
                    "changePercent": round(change_pct, 2),
                    "currency": meta.get('currency', 'USD'),
                    "exchange": meta.get('exchangeName', 'Global Market'),
                    "dayHigh": meta.get('regularMarketDayHigh', price),
                    "dayLow": meta.get('regularMarketDayLow', price),
                    "marketCap": "N/A", 
                    "peRatio": "N/A",
                    "volume": meta.get('regularMarketVolume', 0)
                })
            }
    except Exception as e:
        return { "statusCode": 500, "body": json.dumps({"error": str(e)}) }
