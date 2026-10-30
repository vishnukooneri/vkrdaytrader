import json
import yfinance as yf

def handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    symbol = query_params.get('ticker', 'AAPL')
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
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
        return { "statusCode": 500, "body": json.dumps({"error": str(e)}) }
