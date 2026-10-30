from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import yfinance as yf
import subprocess
import os

app = FastAPI()

# 1. Serve your index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 2. Global Stock Data API
@app.get("/api/stock_data")
async def get_stock_data(ticker: str = Query("AAPL")):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose') or 0
        
        return {
            "symbol": ticker, "name": info.get('shortName') or info.get('longName') or ticker,
            "price": price, "change": info.get('regularMarketChange') or 0,
            "changePercent": info.get('regularMarketChangePercent') or 0,
            "marketCap": info.get('marketCap') or "N/A", "peRatio": info.get('trailingPE') or "N/A",
            "volume": info.get('volume') or 0, "currency": info.get('currency') or "USD",
            "dayHigh": info.get('dayHigh') or price, "dayLow": info.get('dayLow') or price,
            "fiftyTwoWeekHigh": info.get('fiftyTwoWeekHigh') or price,
            "fiftyTwoWeekLow": info.get('fiftyTwoWeekLow') or price,
            "exchange": info.get('fullExchangeName') or "Global Market"
        }
    except Exception as e:
        return {"error": str(e)}

# 3. GitHub Script Bridge (Runs your trader-news script)
@app.get("/api/run_news")
async def run_news(ticker: str = Query("AAPL")):
    script_path = os.path.join(os.getcwd(), 'trader-news', 'news.py')
    try:
        result = subprocess.run(
            ['python3', script_path, '--tickers', ticker, '--hours', '24'],
            capture_output=True, text=True, timeout=15
        )
        return {
            "source": "GitHub Repo: trader-news/news.py",
            "ticker": ticker,
            "terminal_output": result.stdout,
            "errors": result.stderr
        }
    except Exception as e:
        return {"error": str(e)}
