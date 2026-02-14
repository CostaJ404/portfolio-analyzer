"""
Módulo principal para gerenciamento de portfólio de investimentos.
"""
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

from .stock import Stock


class Portfolio:
    """
    Classe principal para gerenciar um portfólio de investimentos.
    
    Attributes:
        name: Nome do portfólio
        stocks: Dicionário de ações {symbol: Stock}
        cash: Caixa disponível
    """
    
    def __init__(self, name: str = "Meu Portfólio", cash: float = 0):
        self.name = name
        self.stocks: Dict[str, Stock] = {}
        self.cash = cash
        self.creation_date = datetime.now()
        self.metadata = {}
    
    def add_stock(
        self,
        symbol: str,
        shares: float,
        purchase_price: float,
        name: Optional[str] = None
    ):
        """Adiciona ou atualiza uma ação no portfólio."""
        symbol = symbol.upper()
        
        if symbol in self.stocks:
            # Atualiza ação existente
            self.stocks[symbol].add_transaction(
                shares=shares,
                price=purchase_price,
                transaction_type='buy'
            )
        else:
            # Cria nova ação
            self.stocks[symbol] = Stock(
                symbol=symbol,
                shares=shares,
                purchase_price=purchase_price,
                name=name
            )
        
        # Deduz do caixa se houver
        cost = shares * purchase_price
        if self.cash >= cost:
            self.cash -= cost
    
    def remove_stock(self, symbol: str):
        """Remove uma ação do portfólio."""
        symbol = symbol.upper()
        if symbol in self.stocks:
            del self.stocks[symbol]
    
    def sell_stock(self, symbol: str, shares: float, price: float):
        """Vende ações de um símbolo específico."""
        symbol = symbol.upper()
        if symbol not in self.stocks:
            raise ValueError(f"Ação {symbol} não encontrada no portfólio")
        
        self.stocks[symbol].add_transaction(
            shares=shares,
            price=price,
            transaction_type='sell'
        )
        
        # Adiciona ao caixa
        self.cash += shares * price
        
        # Remove se não houver mais ações
        if self.stocks[symbol].shares == 0:
            self.remove_stock(symbol)
    
    @property
    def total_value(self) -> float:
        """Valor total do portfólio (ações + caixa)."""
        stocks_value = sum(stock.current_value for stock in self.stocks.values())
        return stocks_value + self.cash
    
    @property
    def total_invested(self) -> float:
        """Total investido (custo base)."""
        return sum(stock.total_invested for stock in self.stocks.values())
    
    @property
    def total_gain_loss(self) -> float:
        """Ganho/perda total em dólares."""
        return self.total_value - self.total_invested - self.cash
    
    @property
    def total_return(self) -> float:
        """Retorno total em percentual."""
        if self.total_invested == 0:
            return 0
        return (self.total_gain_loss / self.total_invested) * 100
    
    def get_allocation(self) -> Dict[str, float]:
        """Retorna a alocação percentual de cada ação."""
        total = self.total_value
        if total == 0:
            return {}
        
        allocation = {}
        for symbol, stock in self.stocks.items():
            allocation[symbol] = (stock.current_value / total) * 100
        
        if self.cash > 0:
            allocation['CASH'] = (self.cash / total) * 100
        
        return allocation
    
    def get_sector_allocation(self) -> Dict[str, float]:
        """Retorna a alocação por setor."""
        sectors = {}
        total = self.total_value
        
        for stock in self.stocks.values():
            info = stock.get_info()
            sector = info.get('sector', 'Unknown')
            value = stock.current_value
            
            if sector in sectors:
                sectors[sector] += value
            else:
                sectors[sector] = value
        
        # Converte para percentual
        return {k: (v / total) * 100 for k, v in sectors.items()}
    
    def calculate_portfolio_returns(self, period: str = "1y") -> pd.Series:
        """Calcula os retornos históricos do portfólio."""
        if not self.stocks:
            return pd.Series()
        
        # Pega os retornos de cada ação
        all_returns = []
        weights = []
        
        for stock in self.stocks.values():
            returns = stock.calculate_returns(period=period)
            if not returns.empty:
                all_returns.append(returns)
                # Peso baseado no valor atual
                weight = stock.current_value / self.total_value
                weights.append(weight)
        
        if not all_returns:
            return pd.Series()
        
        # Combina os retornos
        returns_df = pd.concat(all_returns, axis=1)
        returns_df.fillna(0, inplace=True)
        
        # Calcula retorno ponderado do portfólio
        portfolio_returns = (returns_df * weights).sum(axis=1)
        
        return portfolio_returns
    
    def calculate_metrics(self, period: str = "1y", risk_free_rate: float = 0.02) -> Dict:
        """Calcula métricas de performance do portfólio."""
        returns = self.calculate_portfolio_returns(period=period)
        
        if returns.empty:
            return {
                'total_return': self.total_return,
                'volatility': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'var_95': 0,
            }
        
        # Volatilidade anualizada
        volatility = returns.std() * np.sqrt(252)
        
        # Sharpe Ratio
        excess_return = returns.mean() * 252 - risk_free_rate
        sharpe_ratio = excess_return / volatility if volatility != 0 else 0
        
        # Maximum Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Value at Risk (95%)
        var_95 = np.percentile(returns, 5)
        
        return {
            'total_return': self.total_return,
            'annualized_return': returns.mean() * 252 * 100,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown * 100,
            'var_95': var_95 * 100,
        }
    
    def calculate_correlation_matrix(self, period: str = "1y") -> pd.DataFrame:
        """Calcula a matriz de correlação entre as ações."""
        if len(self.stocks) < 2:
            return pd.DataFrame()
        
        returns_dict = {}
        for symbol, stock in self.stocks.items():
            returns = stock.calculate_returns(period=period)
            if not returns.empty:
                returns_dict[symbol] = returns
        
        if not returns_dict:
            return pd.DataFrame()
        
        returns_df = pd.DataFrame(returns_dict)
        return returns_df.corr()
    
    def analyze(self, period: str = "1y") -> Dict:
        """Análise completa do portfólio."""
        metrics = self.calculate_metrics(period=period)
        allocation = self.get_allocation()
        sector_allocation = self.get_sector_allocation()
        
        # Análise individual das ações
        stocks_analysis = {}
        for symbol, stock in self.stocks.items():
            stocks_analysis[symbol] = stock.get_summary()
        
        return {
            'name': self.name,
            'total_value': self.total_value,
            'total_invested': self.total_invested,
            'total_gain_loss': self.total_gain_loss,
            'total_return': self.total_return,
            'cash': self.cash,
            'metrics': metrics,
            'allocation': allocation,
            'sector_allocation': sector_allocation,
            'stocks': stocks_analysis,
            'num_stocks': len(self.stocks),
        }
    
    def generate_dashboard(self, output_file: str = "dashboard.html"):
        """Gera um dashboard interativo com Plotly."""
        analysis = self.analyze()
        
        # Cria subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Alocação por Ação',
                'Alocação por Setor',
                'Performance das Ações',
                'Retornos Históricos',
                'Matriz de Correlação',
                'Métricas de Risco'
            ),
            specs=[
                [{'type': 'pie'}, {'type': 'pie'}],
                [{'type': 'bar'}, {'type': 'scatter'}],
                [{'type': 'heatmap'}, {'type': 'indicator'}]
            ]
        )
        
        # 1. Alocação por ação
        allocation = analysis['allocation']
        fig.add_trace(
            go.Pie(
                labels=list(allocation.keys()),
                values=list(allocation.values()),
                name="Alocação",
                hovertemplate='%{label}: %{percent}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Alocação por setor
        sector_allocation = analysis['sector_allocation']
        if sector_allocation:
            fig.add_trace(
                go.Pie(
                    labels=list(sector_allocation.keys()),
                    values=list(sector_allocation.values()),
                    name="Setores",
                    hovertemplate='%{label}: %{percent}<extra></extra>'
                ),
                row=1, col=2
            )
        
        # 3. Performance das ações
        stocks_data = analysis['stocks']
        symbols = list(stocks_data.keys())
        returns = [stocks_data[s]['gain_loss_percent'] for s in symbols]
        colors = ['green' if r >= 0 else 'red' for r in returns]
        
        fig.add_trace(
            go.Bar(
                x=symbols,
                y=returns,
                marker_color=colors,
                name="Retorno %",
                hovertemplate='%{x}: %{y:.2f}%<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 4. Retornos históricos
        portfolio_returns = self.calculate_portfolio_returns()
        if not portfolio_returns.empty:
            cumulative = (1 + portfolio_returns).cumprod()
            fig.add_trace(
                go.Scatter(
                    x=cumulative.index,
                    y=cumulative.values,
                    mode='lines',
                    name='Retorno Acumulado',
                    line=dict(color='blue', width=2),
                    hovertemplate='%{x}: %{y:.3f}x<extra></extra>'
                ),
                row=2, col=2
            )
        
        # 5. Matriz de correlação
        corr_matrix = self.calculate_correlation_matrix()
        if not corr_matrix.empty:
            fig.add_trace(
                go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.index,
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.values,
                    texttemplate='%{text:.2f}',
                    hovertemplate='%{y} vs %{x}: %{z:.2f}<extra></extra>'
                ),
                row=3, col=1
            )
        
        # 6. Indicador de Sharpe Ratio
        metrics = analysis['metrics']
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=metrics['sharpe_ratio'],
                title={'text': "Sharpe Ratio"},
                delta={'reference': 1.0},
                gauge={
                    'axis': {'range': [-1, 3]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [-1, 0], 'color': "lightgray"},
                        {'range': [0, 1], 'color': "gray"},
                        {'range': [1, 2], 'color': "lightgreen"},
                        {'range': [2, 3], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 2
                    }
                }
            ),
            row=3, col=2
        )
        
        # Layout
        fig.update_layout(
            title_text=f"Dashboard - {self.name}",
            showlegend=True,
            height=1200,
            template='plotly_white'
        )
        
        # Salva
        fig.write_html(output_file)
        print(f"Dashboard salvo em: {output_file}")
        
        return output_file
    
    def to_dict(self) -> Dict:
        """Converte o portfólio para dicionário."""
        return {
            'name': self.name,
            'cash': self.cash,
            'creation_date': self.creation_date.isoformat(),
            'stocks': {
                symbol: {
                    'shares': stock.shares,
                    'purchase_price': stock.purchase_price,
                }
                for symbol, stock in self.stocks.items()
            },
            'metadata': self.metadata
        }
    
    def save(self, filename: str):
        """Salva o portfólio em arquivo JSON."""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"Portfólio salvo em: {filename}")
    
    @classmethod
    def load(cls, filename: str) -> 'Portfolio':
        """Carrega um portfólio de arquivo JSON."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        portfolio = cls(name=data['name'], cash=data['cash'])
        portfolio.creation_date = datetime.fromisoformat(data['creation_date'])
        portfolio.metadata = data.get('metadata', {})
        
        for symbol, stock_data in data['stocks'].items():
            portfolio.add_stock(
                symbol=symbol,
                shares=stock_data['shares'],
                purchase_price=stock_data['purchase_price']
            )
        
        return portfolio
    
    def __repr__(self):
        return f"Portfolio('{self.name}', {len(self.stocks)} stocks, ${self.total_value:,.2f})"
    
    def __str__(self):
        output = [f"\n{'='*60}"]
        output.append(f"Portfólio: {self.name}")
        output.append(f"{'='*60}")
        output.append(f"Valor Total: ${self.total_value:,.2f}")
        output.append(f"Total Investido: ${self.total_invested:,.2f}")
        output.append(f"Ganho/Perda: ${self.total_gain_loss:,.2f} ({self.total_return:+.2f}%)")
        output.append(f"Caixa: ${self.cash:,.2f}")
        output.append(f"\nAções ({len(self.stocks)}):")
        output.append(f"{'-'*60}")
        
        for symbol, stock in sorted(self.stocks.items()):
            output.append(
                f"{symbol:6s} | {stock.shares:8.2f} shares | "
                f"${stock.current_value:12,.2f} | "
                f"{stock.gain_loss_percent:+7.2f}%"
            )
        
        output.append(f"{'='*60}\n")
        return '\n'.join(output)
