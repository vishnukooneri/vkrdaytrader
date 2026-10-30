import json
import yfinance as yf
import os

# THIS IS THE MAGIC FIX FOR NETLIFY:
# Tell yfinance to use the /tmp folder for cache so it doesn't crash
os.environ['YFINANCE_DATA_DIR'] = '/tmp'
yf.set_tz_cache_location('/tmp')
yf.set_session_cache_location('/tmp')

def handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    symbol = query_params.get('ticker', 'AAPL')
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose') or 0
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "symbol": symbol, "name": info.get('shortName') or info.get('longName') or symbol,
                "price": price, "change": info.get('regularMarketChange') or 0,
                "changePercent": info.get('regularMarketChangePercent') or 0,
                "marketCap": info.get('marketCap') or "N/A", "peRatio": info.get('trailingPE') or "N/A",
                "volume": info.get('volume') or 0, "currency": info.get('currency') or "USD",
                "dayHigh": info.get('dayHigh') or price, "dayLow": info.get('dayLow') or price,
                "fiftyTwoWeekHigh": info.get('fiftyTwoWeekHigh') or price,
                "fiftyTwoWeekLow": info.get('fiftyTwoWeekLow') or price,
                "exchange": info.get('fullExchangeName') or "Global Market"
            })
        }
    except Exception as e:
        # This returns the actual error message as JSON so we can read it!
        return { "statusCode": 500, "body": json.dumps({"error": str(e)}) }
