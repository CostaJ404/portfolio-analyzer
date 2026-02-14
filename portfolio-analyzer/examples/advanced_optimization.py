"""
Exemplo Avançado - Otimização de Portfólio

Este exemplo demonstra técnicas avançadas de análise e otimização.
"""
import sys
sys.path.insert(0, '../src')

from core import Portfolio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class PortfolioOptimizer:
    """
    Otimizador de portfólio usando Teoria Moderna de Portfólio (MPT).
    """
    
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
        self.returns_data = None
        self.cov_matrix = None
    
    def prepare_data(self, period: str = "1y"):
        """Prepara dados históricos para otimização."""
        print("📊 Preparando dados históricos...")
        
        returns_dict = {}
        for symbol, stock in self.portfolio.stocks.items():
            returns = stock.calculate_returns(period=period)
            if not returns.empty:
                returns_dict[symbol] = returns
        
        self.returns_data = pd.DataFrame(returns_dict)
        self.returns_data.fillna(0, inplace=True)
        
        # Calcula matriz de covariância
        self.cov_matrix = self.returns_data.cov() * 252  # Anualizado
        
        print(f"✓ {len(returns_dict)} ações analisadas")
        print(f"✓ {len(self.returns_data)} dias de dados")
    
    def calculate_portfolio_performance(self, weights):
        """Calcula retorno e risco de um portfólio com pesos dados."""
        returns = np.sum(self.returns_data.mean() * weights) * 252
        std = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        return returns, std
    
    def optimize_sharpe_ratio(self, risk_free_rate: float = 0.02):
        """
        Otimiza para maximizar o Sharpe Ratio.
        """
        print("\n🎯 Otimizando para Sharpe Ratio máximo...")
        
        num_assets = len(self.returns_data.columns)
        
        # Simulação Monte Carlo
        num_portfolios = 10000
        results = np.zeros((4, num_portfolios))
        
        for i in range(num_portfolios):
            # Gera pesos aleatórios
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            # Calcula performance
            portfolio_return, portfolio_std = self.calculate_portfolio_performance(weights)
            sharpe = (portfolio_return - risk_free_rate) / portfolio_std
            
            results[0,i] = portfolio_return
            results[1,i] = portfolio_std
            results[2,i] = sharpe
            results[3,i] = i
        
        # Encontra o melhor
        max_sharpe_idx = np.argmax(results[2])
        
        # Reconstrói pesos ótimos
        np.random.seed(int(results[3, max_sharpe_idx]))
        optimal_weights = np.random.random(num_assets)
        optimal_weights /= np.sum(optimal_weights)
        
        return dict(zip(self.returns_data.columns, optimal_weights))
    
    def optimize_min_variance(self):
        """
        Otimiza para minimizar a variância (risco).
        """
        print("\n🛡️ Otimizando para risco mínimo...")
        
        num_assets = len(self.returns_data.columns)
        
        # Simulação Monte Carlo
        num_portfolios = 10000
        min_variance = float('inf')
        optimal_weights = None
        
        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            _, portfolio_std = self.calculate_portfolio_performance(weights)
            
            if portfolio_std < min_variance:
                min_variance = portfolio_std
                optimal_weights = weights
        
        return dict(zip(self.returns_data.columns, optimal_weights))
    
    def optimize_target_return(self, target_return: float = 0.15):
        """
        Otimiza para atingir um retorno alvo com risco mínimo.
        """
        print(f"\n🎯 Otimizando para retorno alvo de {target_return*100}%...")
        
        num_assets = len(self.returns_data.columns)
        
        num_portfolios = 10000
        min_variance = float('inf')
        optimal_weights = None
        
        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            portfolio_return, portfolio_std = self.calculate_portfolio_performance(weights)
            
            # Procura portfólios próximos ao retorno alvo
            if abs(portfolio_return - target_return) < 0.02:
                if portfolio_std < min_variance:
                    min_variance = portfolio_std
                    optimal_weights = weights
        
        if optimal_weights is None:
            print("⚠️ Não foi possível encontrar portfólio com retorno alvo")
            return None
        
        return dict(zip(self.returns_data.columns, optimal_weights))


def compare_allocations(portfolio: Portfolio, allocations: dict):
    """Compara diferentes alocações."""
    print("\n" + "="*80)
    print("COMPARAÇÃO DE ALOCAÇÕES")
    print("="*80)
    
    for name, weights in allocations.items():
        print(f"\n{name}:")
        print("-" * 40)
        
        for symbol, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            print(f"  {symbol:6s}: {weight*100:6.2f}%")


def rebalance_portfolio(portfolio: Portfolio, target_weights: dict):
    """
    Rebalanceia o portfólio para atingir os pesos alvo.
    """
    print("\n" + "="*80)
    print("REBALANCEAMENTO DO PORTFÓLIO")
    print("="*80)
    
    total_value = portfolio.total_value
    
    print(f"\nValor Total do Portfólio: ${total_value:,.2f}")
    print("\nAjustes Necessários:")
    print("-" * 40)
    
    for symbol, target_weight in target_weights.items():
        target_value = total_value * target_weight
        
        if symbol in portfolio.stocks:
            current_value = portfolio.stocks[symbol].current_value
            current_price = portfolio.stocks[symbol].get_current_price()
        else:
            current_value = 0
            # Precisaria buscar preço atual
            print(f"  {symbol}: Nova posição - ${target_value:,.2f}")
            continue
        
        difference = target_value - current_value
        shares_adjustment = difference / current_price
        
        action = "COMPRAR" if shares_adjustment > 0 else "VENDER"
        print(f"  {symbol}: {action} {abs(shares_adjustment):.2f} ações (${abs(difference):,.2f})")


def main():
    print("=" * 80)
    print("EXEMPLO AVANÇADO - OTIMIZAÇÃO DE PORTFÓLIO")
    print("=" * 80)
    
    # 1. Criar portfólio diversificado
    print("\n1. Criando portfólio diversificado...")
    portfolio = Portfolio(name="Portfólio Otimizado", cash=50000)
    
    # Tecnologia
    portfolio.add_stock("AAPL", shares=50, purchase_price=150.00)
    portfolio.add_stock("MSFT", shares=40, purchase_price=380.00)
    portfolio.add_stock("GOOGL", shares=20, purchase_price=140.00)
    
    # Finanças
    portfolio.add_stock("JPM", shares=30, purchase_price=150.00)
    portfolio.add_stock("BAC", shares=100, purchase_price=35.00)
    
    # Saúde
    portfolio.add_stock("JNJ", shares=40, purchase_price=160.00)
    
    # Consumo
    portfolio.add_stock("WMT", shares=50, purchase_price=160.00)
    
    print("✓ 7 ações adicionadas")
    print(f"Valor Total: ${portfolio.total_value:,.2f}")
    
    # 2. Análise inicial
    print("\n2. Análise Inicial:")
    print("-" * 40)
    analysis = portfolio.analyze()
    
    print(f"Retorno Total: {analysis['total_return']:.2f}%")
    print(f"Sharpe Ratio: {analysis['metrics']['sharpe_ratio']:.3f}")
    print(f"Volatilidade: {analysis['metrics']['volatility']*100:.2f}%")
    
    # 3. Otimização
    optimizer = PortfolioOptimizer(portfolio)
    optimizer.prepare_data(period="1y")
    
    # Diferentes estratégias de otimização
    allocations = {}
    
    # Alocação atual
    allocations["Atual"] = portfolio.get_allocation()
    
    # Max Sharpe Ratio
    optimal_sharpe = optimizer.optimize_sharpe_ratio()
    if optimal_sharpe:
        allocations["Max Sharpe Ratio"] = optimal_sharpe
    
    # Min Variance
    optimal_min_var = optimizer.optimize_min_variance()
    if optimal_min_var:
        allocations["Risco Mínimo"] = optimal_min_var
    
    # Target Return (15%)
    optimal_target = optimizer.optimize_target_return(target_return=0.15)
    if optimal_target:
        allocations["Retorno 15%"] = optimal_target
    
    # 4. Comparar alocações
    compare_allocations(portfolio, allocations)
    
    # 5. Simular performance de cada estratégia
    print("\n" + "="*80)
    print("SIMULAÇÃO DE PERFORMANCE")
    print("="*80)
    
    for name, weights in allocations.items():
        if name == "Atual":
            continue
        
        print(f"\n{name}:")
        print("-" * 40)
        
        # Calcula métricas esperadas
        weights_array = np.array([weights.get(s, 0) for s in optimizer.returns_data.columns])
        exp_return, exp_risk = optimizer.calculate_portfolio_performance(weights_array)
        sharpe = (exp_return - 0.02) / exp_risk if exp_risk > 0 else 0
        
        print(f"  Retorno Esperado: {exp_return*100:.2f}%")
        print(f"  Risco (Volatilidade): {exp_risk*100:.2f}%")
        print(f"  Sharpe Ratio: {sharpe:.3f}")
    
    # 6. Recomendação
    print("\n" + "="*80)
    print("RECOMENDAÇÃO")
    print("="*80)
    
    if optimal_sharpe:
        print("\n🎯 Recomendação: Otimização para Max Sharpe Ratio")
        print("\nEsta estratégia oferece o melhor retorno ajustado ao risco.")
        
        # Simula rebalanceamento
        rebalance_portfolio(portfolio, optimal_sharpe)
    
    # 7. Análise de risco por setor
    print("\n" + "="*80)
    print("ANÁLISE DE RISCO POR SETOR")
    print("="*80)
    
    sector_allocation = portfolio.get_sector_allocation()
    print("\nAlocação Atual por Setor:")
    for sector, percent in sorted(sector_allocation.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sector:20s}: {percent:6.2f}%")
        
        if percent > 40:
            print(f"    ⚠️ ALERTA: Concentração alta em {sector}")
    
    # 8. Matriz de correlação
    print("\n" + "="*80)
    print("MATRIZ DE CORRELAÇÃO")
    print("="*80)
    
    corr_matrix = portfolio.calculate_correlation_matrix()
    if not corr_matrix.empty:
        print("\nCorrelações (valores próximos a 1 indicam movimentação similar):")
        print(corr_matrix.round(2))
        
        # Identifica pares altamente correlacionados
        print("\n⚠️ Pares com Alta Correlação (>0.8):")
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                if abs(corr_matrix.iloc[i, j]) > 0.8:
                    print(f"  {corr_matrix.index[i]} <-> {corr_matrix.columns[j]}: "
                          f"{corr_matrix.iloc[i, j]:.3f}")
    
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA!")
    print("="*80)
    
    print("\n📌 Próximos Passos:")
    print("  1. Revisar as alocações recomendadas")
    print("  2. Considerar rebalancear seguindo a estratégia escolhida")
    print("  3. Monitorar performance regularmente")
    print("  4. Ajustar conforme mudanças no mercado")
    print()


if __name__ == "__main__":
    main()
