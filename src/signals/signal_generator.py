import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NumeraiSignalGenerator:
    """
    Generate Numerai signals from analyzed data
    
    Signal Requirements:
    - Range: 0 to 1
    - Format: ticker, signal
    - Quality: correlation with target > 0.01
    """
    
    def __init__(self):
        self.signals = pd.DataFrame()
    
    def generate_from_analysis(self, 
                               news_sentiment: Dict[str, float],
                               fundamentals: Dict[str, Dict],
                               sec_insights: Dict[str, Dict]) -> pd.DataFrame:
        """
        Generate signals combining multiple data sources
        
        Args:
            news_sentiment: {ticker: sentiment_score (-1 to 1)}
            fundamentals: {ticker: {pe_ratio, revenue_growth, ...}}
            sec_insights: {ticker: {filing_quality, key_metrics, ...}}
        
        Returns:
            DataFrame with columns: ticker, signal
        """
        
        signals = []
        
        for ticker in news_sentiment.keys():
            try:
                # Extract features
                sentiment = news_sentiment.get(ticker, 0)
                metrics = fundamentals.get(ticker, {})
                sec_data = sec_insights.get(ticker, {})
                
                # Calculate composite signal
                signal = self._calculate_composite_signal(
                    sentiment=sentiment,
                    pe_ratio=metrics.get('pe_ratio', 20),
                    revenue_growth=metrics.get('revenue_growth_yoy', 0),
                    data_quality=sec_data.get('quality_score', 0.5)
                )
                
                signals.append({
                    'ticker': ticker,
                    'signal': signal,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Error generating signal for {ticker}: {e}")
                continue
        
        self.signals = pd.DataFrame(signals)
        return self.signals
    
    def _calculate_composite_signal(self, 
                                   sentiment: float,
                                   pe_ratio: float,
                                   revenue_growth: float,
                                   data_quality: float) -> float:
        """
        Composite signal calculation
        
        Factors:
        - News sentiment (30%)
        - Valuation (PE ratio) (30%)
        - Growth (revenue) (30%)
        - Data quality (10%)
        """
        
        # Normalize sentiment (-1 to 1) -> (0 to 1)
        sentiment_score = (sentiment + 1) / 2
        
        # Normalize PE ratio (inverse: lower is better)
        pe_score = 1 / (1 + np.exp((pe_ratio - 20) / 10))
        
        # Normalize revenue growth
        growth_score = 1 / (1 + np.exp(-revenue_growth / 10))
        
        # Weighted composite
        composite = (
            0.30 * sentiment_score +
            0.30 * pe_score +
            0.30 * growth_score +
            0.10 * data_quality
        )
        
        # Ensure in range [0, 1]
        return np.clip(composite, 0, 1)
    
    def validate_signals(self) -> bool:
        """Validate signals meet Numerai requirements"""
        
        if self.signals.empty:
            logger.error("No signals generated")
            return False
        
        # Check range
        if not self.signals['signal'].between(0, 1).all():
            logger.error("Signals outside valid range [0, 1]")
            return False
        
        # Check for nulls
        if self.signals['signal'].isnull().any():
            logger.error("Null values in signals")
            return False
        
        logger.info(f"Validated {len(self.signals)} signals")
        return True
    
    def export_for_numerai(self, output_path: str = "signals.csv"):
        """Export signals in Numerai format"""
        
        if not self.validate_signals():
            raise ValueError("Signal validation failed")
        
        # Numerai format: ticker, signal
        export_df = self.signals[['ticker', 'signal']].copy()
        export_df.to_csv(output_path, index=False)
        
        logger.info(f"Exported signals to {output_path}")
        return output_path
