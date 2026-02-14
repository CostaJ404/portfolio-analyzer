"""
Exemplo Completo - Portfolio Analyzer

Este exemplo demonstra todas as funcionalidades principais do sistema.
"""
import sys
sys.path.insert(0, '../src')

from core import Portfolio, Stock

def main():
    print("=" * 70)
    print("PORTFOLIO ANALYZER - EXEMPLO COMPLETO")
    print("=" * 70)
    
    # 1. Criar um novo portfólio
    print("\n1. Criando portfólio...")
    portfolio = Portfolio(name="Portfólio de Tecnologia", cash=10000)
    
    # 2. Adicionar ações
    print("\n2. Adicionando ações ao portfólio...")
    
    # Ações de tecnologia
    portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
    portfolio.add_stock("GOOGL", shares=5, purchase_price=140.00)
    portfolio.add_stock("MSFT", shares=15, purchase_price=380.00)
    portfolio.add_stock("NVDA", shares=8, purchase_price=480.00)
    portfolio.add_stock("META", shares=7, purchase_price=350.00)
    
    print("✓ Ações adicionadas com sucesso!")
    
    # 3. Visualizar o portfólio
    print("\n3. Resumo do Portfólio:")
    print(portfolio)
    
    # 4. Análise detalhada
    print("\n4. Análise Detalhada:")
    analysis = portfolio.analyze(period="1y")
    
    print(f"\n📊 Métricas Gerais:")
    print(f"   Valor Total: ${analysis['total_value']:,.2f}")
    print(f"   Total Investido: ${analysis['total_invested']:,.2f}")
    print(f"   Retorno Total: {analysis['total_return']:.2f}%")
    print(f"   Número de Ações: {analysis['num_stocks']}")
    
    print(f"\n📈 Métricas de Performance:")
    metrics = analysis['metrics']
    print(f"   Retorno Anualizado: {metrics['annualized_return']:.2f}%")
    print(f"   Volatilidade: {metrics['volatility']*100:.2f}%")
    print(f"   Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
    print(f"   Max Drawdown: {metrics['max_drawdown']:.2f}%")
    print(f"   VaR (95%): {metrics['var_95']:.2f}%")
    
    print(f"\n💼 Alocação por Ação:")
    for symbol, allocation in sorted(
        analysis['allocation'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"   {symbol:6s}: {allocation:6.2f}%")
    
    print(f"\n🏢 Alocação por Setor:")
    for sector, allocation in sorted(
        analysis['sector_allocation'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"   {sector:20s}: {allocation:6.2f}%")
    
    # 5. Análise individual das ações
    print(f"\n📋 Performance Individual:")
    print(f"{'Symbol':<8} {'Shares':>10} {'Investido':>15} {'Valor Atual':>15} {'Retorno':>10}")
    print("-" * 70)
    
    for symbol, stock_data in sorted(analysis['stocks'].items()):
        print(f"{symbol:<8} {stock_data['shares']:>10.2f} "
              f"${stock_data['total_invested']:>14,.2f} "
              f"${stock_data['current_value']:>14,.2f} "
              f"{stock_data['gain_loss_percent']:>9.2f}%")
    
    # 6. Matriz de correlação
    print(f"\n🔗 Matriz de Correlação:")
    corr_matrix = portfolio.calculate_correlation_matrix(period="1y")
    if not corr_matrix.empty:
        print(corr_matrix.round(2).to_string())
    
    # 7. Análise de risco individual
    print(f"\n⚠️  Análise de Risco por Ação:")
    print(f"{'Symbol':<8} {'Volatilidade':>15} {'Sharpe Ratio':>15}")
    print("-" * 40)
    
    for symbol, stock_data in sorted(analysis['stocks'].items()):
        print(f"{symbol:<8} {stock_data['volatility']*100:>14.2f}% "
              f"{stock_data['sharpe_ratio']:>14.3f}")
    
    # 8. Gerar dashboard
    print("\n5. Gerando dashboard interativo...")
    dashboard_file = portfolio.generate_dashboard("portfolio_dashboard.html")
    print(f"✓ Dashboard gerado: {dashboard_file}")
    
    # 9. Salvar portfólio
    print("\n6. Salvando portfólio...")
    portfolio.save("my_portfolio.json")
    print("✓ Portfólio salvo em: my_portfolio.json")
    
    # 10. Demonstrar compra adicional
    print("\n7. Demonstrando compra adicional de ações...")
    print("   Comprando mais 5 ações de AAPL...")
    portfolio.add_stock("AAPL", shares=5, purchase_price=155.00)
    
    aapl = portfolio.stocks["AAPL"]
    print(f"   AAPL agora: {aapl.shares} ações @ ${aapl.purchase_price:.2f} (preço médio)")
    
    # 11. Demonstrar venda
    print("\n8. Demonstrando venda de ações...")
    print("   Vendendo 3 ações de MSFT...")
    current_price = portfolio.stocks["MSFT"].get_current_price()
    portfolio.sell_stock("MSFT", shares=3, price=current_price)
    print(f"   ✓ Vendidas 3 ações de MSFT por ${current_price:.2f}")
    print(f"   Caixa disponível: ${portfolio.cash:.2f}")
    
    # 12. Carregar portfólio salvo
    print("\n9. Testando carregamento de portfólio...")
    loaded_portfolio = Portfolio.load("my_portfolio.json")
    print(f"   ✓ Portfólio carregado: {loaded_portfolio.name}")
    print(f"   Total de ações: {len(loaded_portfolio.stocks)}")
    
    print("\n" + "=" * 70)
    print("EXEMPLO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print("\n📌 Próximos Passos:")
    print("   1. Abra 'portfolio_dashboard.html' no navegador para ver o dashboard")
    print("   2. Explore 'my_portfolio.json' para ver os dados salvos")
    print("   3. Modifique este script para testar suas próprias ações")
    print("   4. Leia a documentação em docs/ para recursos avançados")
    print("\n")

if __name__ == "__main__":
    main()
