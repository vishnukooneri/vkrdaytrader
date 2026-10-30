exports.handler = async (event, context) => {
    const symbol = event.queryStringParameters?.ticker || 'AAPL';
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?interval=1d&range=5d`;

    try {
        const response = await fetch(url, {
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });
        
        if (!response.ok) throw new Error(`Market API error: ${response.status}`);
        
        const data = await response.json();
        const meta = data.chart.result[0].meta;
        
        const price = meta.regularMarketPrice || 0;
        const prevClose = meta.previousClose || 0;
        const change = price - prevClose;
        const changePercent = prevClose ? (change / prevClose) * 100 : 0;

        return {
            statusCode: 200,
            body: JSON.stringify({
                symbol: symbol,
                name: meta.symbol || symbol,
                price: price,
                change: change.toFixed(2),
                changePercent: changePercent.toFixed(2),
                currency: meta.currency || 'USD',
                exchange: meta.exchangeName || 'Global Market',
                dayHigh: meta.regularMarketDayHigh || price,
                dayLow: meta.regularMarketDayLow || price,
                marketCap: "N/A",
                peRatio: "N/A",
                volume: meta.regularMarketVolume || 0
            })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
