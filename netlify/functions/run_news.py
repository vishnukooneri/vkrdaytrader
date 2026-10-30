import json
import subprocess
import os

def handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    ticker = query_params.get('ticker', 'AAPL')
    
    # Point directly to YOUR original GitHub script
    script_path = os.path.join(os.getcwd(), 'trader-news', 'news.py')
    
    try:
        # Run your actual GitHub code
        result = subprocess.run(
            ['python3', script_path, '--tickers', ticker, '--hours', '24'],
            capture_output=True, text=True, timeout=15
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "source": "GitHub Repo: trader-news/news.py",
                "ticker": ticker,
                "terminal_output": result.stdout,
                "errors": result.stderr
            })
        }
    except Exception as e:
        return { "statusCode": 500, "body": json.dumps({"error": str(e)}) }
