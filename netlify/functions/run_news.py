import json
import subprocess
import os

def handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    ticker = query_params.get('ticker', 'AAPL')
    
    script_path = os.path.join(os.getcwd(), 'trader-news', 'news.py')
    
    try:
        # We added "--state /tmp/news.json" so the script saves its memory 
        # in Netlify's temporary folder instead of your read-only repository folder.
        result = subprocess.run(
            ['python3', script_path, '--tickers', ticker, '--hours', '24', '--state', '/tmp/news.json'],
            capture_output=True, 
            text=True, 
            timeout=15
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
