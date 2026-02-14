"""
Testes unitários para Portfolio Analyzer
"""
import pytest
import sys
sys.path.insert(0, '../src')

from core import Portfolio, Stock
from datetime import datetime


class TestStock:
    """Testes para a classe Stock"""
    
    def test_stock_creation(self):
        """Testa criação de uma ação"""
        stock = Stock(symbol="AAPL", shares=10, purchase_price=150.00)
        
        assert stock.symbol == "AAPL"
        assert stock.shares == 10
        assert stock.purchase_price == 150.00
        assert stock.total_invested == 1500.00
    
    def test_stock_add_transaction(self):
        """Testa adição de transações"""
        stock = Stock(symbol="AAPL", shares=10, purchase_price=150.00)
        
        # Compra adicional
        stock.add_transaction(shares=5, price=155.00, transaction_type='buy')
        
        assert stock.shares == 15
        assert len(stock.transactions) == 2
        
        # Verifica preço médio
        expected_avg = (10 * 150 + 5 * 155) / 15
        assert abs(stock.purchase_price - expected_avg) < 0.01
    
    def test_stock_sell_transaction(self):
        """Testa venda de ações"""
        stock = Stock(symbol="AAPL", shares=10, purchase_price=150.00)
        
        # Venda
        stock.add_transaction(shares=3, price=160.00, transaction_type='sell')
        
        assert stock.shares == 7
        assert len(stock.transactions) == 2
    
    def test_stock_sell_more_than_owned(self):
        """Testa venda de mais ações do que possui"""
        stock = Stock(symbol="AAPL", shares=10, purchase_price=150.00)
        
        with pytest.raises(ValueError):
            stock.add_transaction(shares=15, price=160.00, transaction_type='sell')
    
    def test_stock_current_value(self):
        """Testa cálculo do valor atual"""
        stock = Stock(symbol="AAPL", shares=10, purchase_price=150.00)
        
        # Mock do preço atual
        current_value = stock.current_value
        assert current_value >= 0  # Preço real da API
    
    def test_stock_gain_loss_percent(self):
        """Testa cálculo de ganho/perda percentual"""
        stock = Stock(symbol="AAPL", shares=10, purchase_price=100.00)
        
        # O valor real depende da API
        gain_loss_percent = stock.gain_loss_percent
        assert isinstance(gain_loss_percent, (int, float))


class TestPortfolio:
    """Testes para a classe Portfolio"""
    
    def test_portfolio_creation(self):
        """Testa criação de portfólio"""
        portfolio = Portfolio(name="Test Portfolio", cash=10000)
        
        assert portfolio.name == "Test Portfolio"
        assert portfolio.cash == 10000
        assert len(portfolio.stocks) == 0
    
    def test_add_stock_to_portfolio(self):
        """Testa adição de ações ao portfólio"""
        portfolio = Portfolio(name="Test Portfolio", cash=10000)
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        
        assert "AAPL" in portfolio.stocks
        assert portfolio.stocks["AAPL"].shares == 10
        # Verifica dedução do caixa
        assert portfolio.cash == 10000 - (10 * 150)
    
    def test_add_multiple_stocks(self):
        """Testa adição de múltiplas ações"""
        portfolio = Portfolio(name="Test Portfolio", cash=20000)
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        portfolio.add_stock("GOOGL", shares=5, purchase_price=2800.00)
        portfolio.add_stock("MSFT", shares=15, purchase_price=300.00)
        
        assert len(portfolio.stocks) == 3
        assert "AAPL" in portfolio.stocks
        assert "GOOGL" in portfolio.stocks
        assert "MSFT" in portfolio.stocks
    
    def test_remove_stock(self):
        """Testa remoção de ações"""
        portfolio = Portfolio(name="Test Portfolio")
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        assert "AAPL" in portfolio.stocks
        
        portfolio.remove_stock("AAPL")
        assert "AAPL" not in portfolio.stocks
    
    def test_sell_stock(self):
        """Testa venda de ações"""
        portfolio = Portfolio(name="Test Portfolio", cash=0)
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        initial_shares = portfolio.stocks["AAPL"].shares
        
        # Vende metade
        portfolio.sell_stock("AAPL", shares=5, price=160.00)
        
        assert portfolio.stocks["AAPL"].shares == initial_shares - 5
        assert portfolio.cash == 5 * 160.00
    
    def test_sell_all_shares_removes_stock(self):
        """Testa que vender todas as ações remove do portfólio"""
        portfolio = Portfolio(name="Test Portfolio")
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        portfolio.sell_stock("AAPL", shares=10, price=160.00)
        
        assert "AAPL" not in portfolio.stocks
    
    def test_total_value(self):
        """Testa cálculo do valor total"""
        portfolio = Portfolio(name="Test Portfolio", cash=5000)
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        
        total_value = portfolio.total_value
        assert total_value >= 5000  # Caixa + valor das ações
    
    def test_allocation(self):
        """Testa cálculo de alocação"""
        portfolio = Portfolio(name="Test Portfolio", cash=1000)
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        portfolio.add_stock("GOOGL", shares=5, purchase_price=140.00)
        
        allocation = portfolio.get_allocation()
        
        assert "AAPL" in allocation
        assert "GOOGL" in allocation
        assert "CASH" in allocation
        
        # Soma deve ser ~100%
        total = sum(allocation.values())
        assert abs(total - 100) < 0.01
    
    def test_save_and_load(self, tmp_path):
        """Testa salvamento e carregamento de portfólio"""
        # Cria portfólio
        portfolio = Portfolio(name="Test Portfolio", cash=5000)
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        portfolio.add_stock("GOOGL", shares=5, purchase_price=140.00)
        
        # Salva
        file_path = tmp_path / "test_portfolio.json"
        portfolio.save(str(file_path))
        
        # Carrega
        loaded = Portfolio.load(str(file_path))
        
        assert loaded.name == portfolio.name
        assert loaded.cash == portfolio.cash
        assert len(loaded.stocks) == len(portfolio.stocks)
        assert "AAPL" in loaded.stocks
        assert "GOOGL" in loaded.stocks
    
    def test_analyze(self):
        """Testa análise completa do portfólio"""
        portfolio = Portfolio(name="Test Portfolio", cash=1000)
        
        portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
        portfolio.add_stock("GOOGL", shares=5, purchase_price=140.00)
        
        analysis = portfolio.analyze()
        
        assert 'name' in analysis
        assert 'total_value' in analysis
        assert 'metrics' in analysis
        assert 'allocation' in analysis
        assert 'stocks' in analysis
        
        # Verifica métricas
        metrics = analysis['metrics']
        assert 'total_return' in metrics
        assert 'volatility' in metrics
        assert 'sharpe_ratio' in metrics


class TestTransaction:
    """Testes para transações"""
    
    def test_transaction_total_cost(self):
        """Testa cálculo do custo total da transação"""
        from core import Transaction
        
        transaction = Transaction(
            date=datetime.now(),
            shares=10,
            price=150.00,
            transaction_type='buy',
            fees=10.00
        )
        
        expected_cost = (10 * 150) + 10
        assert transaction.total_cost == expected_cost


def test_portfolio_string_representation():
    """Testa representação em string do portfólio"""
    portfolio = Portfolio(name="Test Portfolio", cash=5000)
    portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
    
    string_repr = str(portfolio)
    
    assert "Test Portfolio" in string_repr
    assert "AAPL" in string_repr
    assert "5000" in string_repr or "5,000" in string_repr


def test_portfolio_repr():
    """Testa __repr__ do portfólio"""
    portfolio = Portfolio(name="Test Portfolio", cash=5000)
    portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
    
    repr_str = repr(portfolio)
    
    assert "Portfolio" in repr_str
    assert "Test Portfolio" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
