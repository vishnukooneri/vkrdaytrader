from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import json
import urllib.request

app = Flask(__name__)

# 1. Serve the Website (index.html)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 2. Stock Data API (Connects to Yahoo Finance)
@app.route('/api/stock_data')
def stock_data():
    symbol = request.args.get('ticker', 'AAPL')
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
            
            return jsonify({
                "symbol": symbol, "name": meta.get('symbol', symbol),
                "price": price, "change": round(change, 2),
                "changePercent": round(change_pct, 2),
                "currency": meta.get('currency', 'USD'),
                "exchange": meta.get('exchangeName', 'Global Market'),
                "dayHigh": meta.get('regularMarketDayHigh', price),
                "dayLow": meta.get('regularMarketDayLow', price),
                "marketCap": "N/A", "peRatio": "N/A",
                "volume": meta.get('regularMarketVolume', 0)
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Run Your GitHub Python Scripts (The Magic Part!)
@app.route('/api/run_news')
def run_news():
    ticker = request.args.get('ticker', 'AAPL')
    script_path = os.path.join(os.getcwd(), 'trader-news', 'news.py')
    
    try:
        # This actually runs your original GitHub code!
        result = subprocess.run(
            ['python3', script_path, '--tickers', ticker, '--hours', '24', '--state', '/tmp/news.json'],
            capture_output=True, text=True, timeout=15
        )
        return jsonify({
            "source": "GitHub Repo: trader-news/news.py",
            "ticker": ticker,
            "terminal_output": result.stdout,
            "errors": result.stderr
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render requires the server to run on 0.0.0.0 and the PORT environment variable
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
