import finnhub
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class FinnhubDataFetcher:
    """
    Finnhub free tier data fetcher
    - 60 requests/minute
    - Company fundamentals
    - Basic financial metrics
    """
    
    def __init__(self, api_key: str):
        self.client = finnhub.Client(api_key=api_key)
        self.request_count = 0
        self.last_request_time = datetime.now()
    
    def get_company_profile(self, ticker: str) -> Dict:
        """Fetch company profile and basic info"""
        try:
            profile = self.client.company_profile2(symbol=ticker)
            self._track_request()
            return profile
        except Exception as e:
            logger.error(f"Error fetching profile for {ticker}: {e}")
            return {}
    
    def get_financial_metrics(self, ticker: str) -> Dict:
        """Fetch key financial metrics"""
        try:
            metrics = self.client.company_basic_financials(ticker, 'all')
            self._track_request()
            return metrics
        except Exception as e:
            logger.error(f"Error fetching metrics for {ticker}: {e}")
            return {}
    
    def get_quote(self, ticker: str) -> Dict:
        """Fetch current stock quote"""
        try:
            quote = self.client.quote(ticker)
            self._track_request()
            return quote
        except Exception as e:
            logger.error(f"Error fetching quote for {ticker}: {e}")
            return {}
    
    def batch_quotes(self, tickers: List[str]) -> Dict[str, Dict]:
        """Fetch quotes for multiple tickers"""
        results = {}
        for ticker in tickers:
            results[ticker] = self.get_quote(ticker)
        return results
    
    def _track_request(self):
        """Track API request count (rate limiting)"""
        self.request_count += 1
        current_time = datetime.now()
        elapsed = (current_time - self.last_request_time).total_seconds()
        
        if elapsed >= 60:
            logger.info(f"Rate: {self.request_count} requests in {elapsed:.1f}s")
            self.request_count = 0
            self.last_request_time = current_time
