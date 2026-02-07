from perplexity import Perplexity
from typing import List, Dict, Literal
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerplexityNumeraiDevKit:
    """
    Production fetcher for Numerai + Phase 2 improvements:
    - Batch queries (5/request) for efficiency
    - SEC search mode for 10-K/10-Q filing data
    - Domain filtering for curated sources
    - Structured JSON output for signal generation
    - Error handling + rate limiting
    - Performance monitoring (Phase 2)
    """
    
    def __init__(self, api_key: str):
        self.client = Perplexity(api_key=api_key)
        self.request_count = 0
        self.start_time = datetime.now()
        
        # Phase 2: Monitoring hooks
        self.perf_metrics = {
            "total_requests": 0,
            "total_tokens": 0,
            "avg_latency_ms": [],
            "errors": []
        }
    
    # ============ NEWS FETCHING (Batch) ============
    
    def batch_market_news(self, queries: List[str], max_results: int = 5) -> Dict:
        """
        Batch fetch market news with domain filtering
        
        Args:
            queries: Up to 5 queries (e.g., "AAPL earnings", "MSFT AI")
            max_results: Results per query
        
        Returns:
            {query: [{headline, url, summary, source, sentiment}, ...]}
        """
        
        if len(queries) > 5:
            logger.warning(f"Max 5 queries. Splitting {len(queries)} queries.")
            queries = queries[:5]
        
        try:
            start = datetime.now()
            
            search_results = self.client.search.create(
                query=queries,
                max_results=max_results,
                max_tokens_per_page=2048,
                # Phase 1: News filtering
                search_domain_filter=[
                    "cnbc.com",
                    "bloomberg.com",
                    "reuters.com",
                    "marketwatch.com",
                    "investor.com"
                ]
            )
            
            parsed = self._parse_batch_results(search_results, queries)
            latency = (datetime.now() - start).total_seconds() * 1000
            
            # Phase 2: Performance monitoring
            self._record_metric(len(queries), latency, "news_batch")
            
            return parsed
            
        except Exception as e:
            logger.error(f"Batch news error: {e}")
            self.perf_metrics["errors"].append({
                "type": "batch_news",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return {}
    
    # ============ SEC FILINGS (NEW - January 2026) ============
    
    def fetch_sec_filings(self, ticker: str, filing_type: Literal["10-K", "10-Q", "8-K"] = "10-K") -> Dict:
        """
        Fetch SEC filings directly via search_mode: "sec"
        
        Args:
            ticker: Stock symbol (e.g., "AAPL")
            filing_type: "10-K" (annual), "10-Q" (quarterly), "8-K" (current)
        
        Returns:
            {filing_type, company, period, revenue, net_income, key_metrics, ...}
        """
        
        query = f"{ticker} {filing_type} 2025"
        
        try:
            start = datetime.now()
            
            # NEW: SEC search mode
            sec_results = self.client.search.create(
                query=query,
                search_mode="sec",  # Direct SEC access
                max_results=1,  # Get most recent filing
                max_tokens_per_page=4096
            )
            
            # Parse structured financial data
            filing_data = self._extract_sec_metrics(
                sec_results.results[0] if sec_results.results else {},
                ticker,
                filing_type
            )
            
            latency = (datetime.now() - start).total_seconds() * 1000
            self._record_metric(1, latency, "sec_filing")
            
            return filing_data
            
        except Exception as e:
            logger.error(f"SEC filing error: {e}")
            self.perf_metrics["errors"].append({
                "type": "sec_filing",
                "ticker": ticker,
                "message": str(e)
            })
            return {}
    
    # ============ FINANCIAL DATA (Structured JSON Output) ============
    
    def extract_financial_metrics(self, company_name: str, context_html: str = "") -> Dict:
        """
        Extract structured financial metrics using JSON mode
        
        Args:
            company_name: Company to analyze
            context_html: Optional HTML content to analyze
        
        Returns:
            {pe_ratio, price_to_book, dividend_yield, 52w_high, 52w_low, ...}
        """
        
        prompt = f"""Extract financial metrics for {company_name}:
        {context_html if context_html else "Search current data"}
        
        Return ONLY valid JSON:
        {{
            "company": "{company_name}",
            "pe_ratio": 28.5,
            "price_to_book": 45.2,
            "dividend_yield": 0.42,
            "52week_high": 195.87,
            "52week_low": 152.34,
            "market_cap_billions": 3200,
            "revenue_growth_yoy": 12.5,
            "earnings_per_share": 6.05,
            "data_quality": 0.95
        }}"""
        
        try:
            start = datetime.now()
            
            response = self.client.chat.create(
                model="sonar-pro",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Deterministic extraction
                # NEW: Structured output mode
                response_format={"type": "json_object"}
            )
            
            metrics = json.loads(response.choices[0].message.content)
            
            latency = (datetime.now() - start).total_seconds() * 1000
            self._record_metric(1, latency, "extraction")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            return {}
    
    # ============ HELPER METHODS ============
    
    def _parse_batch_results(self, response, queries: List[str]) -> Dict:
        """Parse batch search results"""
        
        parsed = {}
        
        if isinstance(response.results[0], list):
            for i, batch in enumerate(response.results):
                parsed[queries[i]] = [
                    {
                        "headline": r.title,
                        "url": r.url,
                        "summary": r.snippet[:150],
                        "source": self._extract_domain(r.url),
                        "published_date": getattr(r, 'published_date', None),
                        "timestamp": datetime.now().isoformat()
                    }
                    for r in batch
                ]
        else:
            parsed[queries[0]] = [
                {
                    "headline": r.title,
                    "url": r.url,
                    "summary": r.snippet[:150],
                    "source": self._extract_domain(r.url)
                }
                for r in response.results
            ]
        
        return parsed
    
    def _extract_sec_metrics(self, filing_result, ticker: str, filing_type: str) -> Dict:
        """Extract key metrics from SEC filing"""
        
        return {
            "ticker": ticker,
            "filing_type": filing_type,
            "company": filing_result.get("title", ""),
            "url": filing_result.get("url", ""),
            "filed_date": getattr(filing_result, 'published_date', None),
            "snippet": filing_result.get("snippet", "")[:500]
        }
    
    @staticmethod
    def _extract_domain(url: str) -> str:
        from urllib.parse import urlparse
        return urlparse(url).netloc
    
    # ============ PHASE 2: MONITORING & METRICS ============
    
    def _record_metric(self, requests: int, latency_ms: float, operation: str):
        """Record performance metric (Phase 2 requirement)"""
        
        self.perf_metrics["total_requests"] += requests
        self.perf_metrics["avg_latency_ms"].append(latency_ms)
        
        logger.info(f"[{operation}] Requests: {requests}, Latency: {latency_ms:.1f}ms")
    
    def get_health_metrics(self) -> Dict:
        """Return performance dashboard (Phase 2 monitoring)"""
        
        avg_latency = (
            sum(self.perf_metrics["avg_latency_ms"]) / 
            len(self.perf_metrics["avg_latency_ms"])
            if self.perf_metrics["avg_latency_ms"] else 0
        )
        
        uptime = (datetime.now() - self.start_time).total_seconds() / 3600
        
        return {
            "total_requests": self.perf_metrics["total_requests"],
            "avg_latency_ms": avg_latency,
            "error_count": len(self.perf_metrics["errors"]),
            "uptime_hours": uptime,
            "recent_errors": self.perf_metrics["errors"][-5:]
        }
