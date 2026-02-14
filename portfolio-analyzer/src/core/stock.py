"""
Módulo para gerenciamento de ações individuais.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import yfinance as yf
import pandas as pd
import numpy as np
from dataclasses import dataclass, field


@dataclass
class Transaction:
    """Representa uma transação de compra/venda."""
    date: datetime
    shares: float
    price: float
    transaction_type: str  # 'buy' or 'sell'
    fees: float = 0.0
    
    @property
    def total_cost(self) -> float:
        """Custo total incluindo taxas."""
        return (self.shares * self.price) + self.fees


class Stock:
    """
    Classe para gerenciar uma ação individual no portfólio.
    
    Attributes:
        symbol: Ticker da ação (ex: 'AAPL', 'GOOGL')
        shares: Número de ações possuídas
        purchase_price: Preço médio de compra
        transactions: Histórico de transações
    """
    
    def __init__(
        self,
        symbol: str,
        shares: float = 0,
        purchase_price: float = 0,
        name: Optional[str] = None
    ):
        self.symbol = symbol.upper()
        self.shares = shares
        self.purchase_price = purchase_price
        self.name = name
        self.transactions: List[Transaction] = []
        self._ticker = None
        self._cache = {}
        self._cache_time = {}
        
        # Adiciona transação inicial se houver
        if shares > 0 and purchase_price > 0:
            self.add_transaction(
                shares=shares,
                price=purchase_price,
                transaction_type='buy',
                date=datetime.now()
            )
    
    @property
    def ticker(self):
        """Lazy loading do objeto ticker do yfinance."""
        if self._ticker is None:
            self._ticker = yf.Ticker(self.symbol)
        return self._ticker
    
    def _get_cached(self, key: str, ttl: int = 300):
        """Retorna dados do cache se ainda válidos."""
        if key in self._cache:
            if datetime.now() - self._cache_time.get(key, datetime.min) < timedelta(seconds=ttl):
                return self._cache[key]
        return None
    
    def _set_cache(self, key: str, value):
        """Armazena dados no cache."""
        self._cache[key] = value
        self._cache_time[key] = datetime.now()
    
    def add_transaction(
        self,
        shares: float,
        price: float,
        transaction_type: str,
        date: Optional[datetime] = None,
        fees: float = 0.0
    ):
        """Adiciona uma transação ao histórico."""
        if date is None:
            date = datetime.now()
        
        transaction = Transaction(
            date=date,
            shares=shares,
            price=price,
            transaction_type=transaction_type,
            fees=fees
        )
        
        self.transactions.append(transaction)
        
        # Atualiza o total de ações e preço médio
        if transaction_type == 'buy':
            total_cost = (self.shares * self.purchase_price) + transaction.total_cost
            self.shares += shares
            self.purchase_price = total_cost / self.shares if self.shares > 0 else 0
        elif transaction_type == 'sell':
            self.shares -= shares
            if self.shares < 0:
                raise ValueError("Não é possível vender mais ações do que possui")
    
    def get_current_price(self) -> float:
        """Obtém o preço atual da ação."""
        cached = self._get_cached('current_price', ttl=60)
        if cached is not None:
            return cached
        
        try:
            info = self.ticker.info
            price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            self._set_cache('current_price', price)
            return price
        except Exception as e:
            print(f"Erro ao obter preço de {self.symbol}: {e}")
            return 0
    
    def get_info(self) -> Dict:
        """Obtém informações detalhadas da ação."""
        cached = self._get_cached('info', ttl=3600)
        if cached is not None:
            return cached
        
        try:
            info = self.ticker.info
            self._set_cache('info', info)
            return info
        except Exception as e:
            print(f"Erro ao obter informações de {self.symbol}: {e}")
            return {}
    
    def get_historical_data(
        self,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Obtém dados históricos da ação.
        
        Args:
            period: Período ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval: Intervalo ('1m', '5m', '15m', '1h', '1d', '1wk', '1mo')
        """
        cache_key = f'history_{period}_{interval}'
        cached = self._get_cached(cache_key, ttl=3600)
        if cached is not None:
            return cached
        
        try:
            history = self.ticker.history(period=period, interval=interval)
            self._set_cache(cache_key, history)
            return history
        except Exception as e:
            print(f"Erro ao obter histórico de {self.symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_returns(self, period: str = "1y") -> pd.Series:
        """Calcula os retornos diários."""
        history = self.get_historical_data(period=period)
        if history.empty:
            return pd.Series()
        return history['Close'].pct_change().dropna()
    
    def calculate_volatility(self, period: str = "1y", annualized: bool = True) -> float:
        """Calcula a volatilidade (desvio padrão dos retornos)."""
        returns = self.calculate_returns(period=period)
        if returns.empty:
            return 0
        
        volatility = returns.std()
        if annualized:
            volatility *= np.sqrt(252)  # 252 dias de negociação
        
        return volatility
    
    def calculate_sharpe_ratio(
        self,
        period: str = "1y",
        risk_free_rate: float = 0.02
    ) -> float:
        """
        Calcula o Sharpe Ratio.
        
        Args:
            period: Período de análise
            risk_free_rate: Taxa livre de risco anualizada
        """
        returns = self.calculate_returns(period=period)
        if returns.empty:
            return 0
        
        excess_returns = returns.mean() * 252 - risk_free_rate
        volatility = self.calculate_volatility(period=period)
        
        if volatility == 0:
            return 0
        
        return excess_returns / volatility
    
    @property
    def current_value(self) -> float:
        """Valor atual do investimento."""
        return self.shares * self.get_current_price()
    
    @property
    def total_invested(self) -> float:
        """Total investido (custo base)."""
        return self.shares * self.purchase_price
    
    @property
    def gain_loss(self) -> float:
        """Ganho ou perda em dólares."""
        return self.current_value - self.total_invested
    
    @property
    def gain_loss_percent(self) -> float:
        """Ganho ou perda em percentual."""
        if self.total_invested == 0:
            return 0
        return (self.gain_loss / self.total_invested) * 100
    
    def get_summary(self) -> Dict:
        """Retorna um resumo completo da ação."""
        info = self.get_info()
        
        return {
            'symbol': self.symbol,
            'name': self.name or info.get('longName', self.symbol),
            'shares': self.shares,
            'purchase_price': self.purchase_price,
            'current_price': self.get_current_price(),
            'current_value': self.current_value,
            'total_invested': self.total_invested,
            'gain_loss': self.gain_loss,
            'gain_loss_percent': self.gain_loss_percent,
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0),
            'volatility': self.calculate_volatility(),
            'sharpe_ratio': self.calculate_sharpe_ratio(),
        }
    
    def __repr__(self):
        return f"Stock({self.symbol}, shares={self.shares}, price=${self.purchase_price:.2f})"
    
    def __str__(self):
        return (f"{self.symbol}: {self.shares} shares @ ${self.purchase_price:.2f} "
                f"(Current: ${self.get_current_price():.2f})")
