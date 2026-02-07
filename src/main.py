import os
import logging
from dotenv import load_dotenv
import argparse
from datetime import datetime

from data.perplexity_devkit import PerplexityNumeraiDevKit
from data.finnhub_fetcher import FinnhubDataFetcher
from signals.signal_generator import NumeraiSignalGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/numerai.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main(mode: str = "production", date: str = None):
    """
    Main orchestration function
    
    Args:
        mode: 'production' or 'test'
        date: Target date for signal generation (YYYY-MM-DD)
    """
    
    logger.info(f"Starting Numerai Agentic AI - Mode: {mode}")
    
    # Initialize components
    perplexity = PerplexityNumeraiDevKit(
        api_key=os.getenv("PERPLEXITY_API_KEY")
    )
    
    finnhub = FinnhubDataFetcher(
        api_key=os.getenv("FINNHUB_API_KEY")
    )
    
    signal_gen = NumeraiSignalGenerator()
    
    # Watchlist
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
        "TSLA", "META", "BRK.B", "JNJ", "V"
    ]
    
    logger.info(f"Processing {len(tickers)} tickers")
    
    # Step 1: Fetch news (Perplexity batch)
    logger.info("Fetching market news...")
    news_queries = [f"{ticker} market analysis February 2026" for ticker in tickers[:5]]
    news_data = perplexity.batch_market_news(news_queries, max_results=3)
    
    # Step 2: Fetch SEC filings
    logger.info("Fetching SEC filings...")
    sec_data = {}
    for ticker in tickers[:3]:
        filing = perplexity.fetch_sec_filings(ticker, "10-Q")
        sec_data[ticker] = filing
    
    # Step 3: Fetch fundamentals (Finnhub)
    logger.info("Fetching fundamentals...")
    fundamentals = {}
    for ticker in tickers:
        metrics = finnhub.get_financial_metrics(ticker)
        fundamentals[ticker] = metrics
    
    # Step 4: Generate signals
    logger.info("Generating signals...")
    
    # Mock sentiment for demo (in production: use LLM analysis)
    news_sentiment = {ticker: 0.6 for ticker in tickers}
    
    signals = signal_gen.generate_from_analysis(
        news_sentiment=news_sentiment,
        fundamentals=fundamentals,
        sec_insights=sec_data
    )
    
    # Step 5: Export signals
    output_path = signal_gen.export_for_numerai("data/signals/output.csv")
    logger.info(f"Signals exported to {output_path}")
    
    # Step 6: Health check
    health = perplexity.get_health_metrics()
    logger.info(f"Health metrics: {health}")
    
    logger.info("Pipeline complete")
    
    return {
        "signals": signals,
        "health": health,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Numerai Agentic AI System")
    parser.add_argument("--mode", choices=["production", "test"], default="production")
    parser.add_argument("--date", type=str, help="Target date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    main(mode=args.mode, date=args.date)
