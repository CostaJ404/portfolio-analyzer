# 🚀 Guia de Início Rápido - Portfolio Analyzer

Este guia vai te ajudar a começar em **5 minutos**!

## Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/portfolio-analyzer.git
cd portfolio-analyzer

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
```

## Seu Primeiro Portfólio em 2 Minutos

Crie um arquivo `quick_start.py`:

```python
from src.core import Portfolio

# 1. Crie um portfólio
portfolio = Portfolio(name="Meu Primeiro Portfólio", cash=10000)

# 2. Adicione algumas ações
portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)  # Apple
portfolio.add_stock("GOOGL", shares=5, purchase_price=140.00)  # Google
portfolio.add_stock("MSFT", shares=15, purchase_price=380.00)  # Microsoft

# 3. Veja o resultado
print(portfolio)

# 4. Análise rápida
analysis = portfolio.analyze()
print(f"\n💰 Valor Total: ${analysis['total_value']:,.2f}")
print(f"📈 Retorno: {analysis['total_return']:.2f}%")

# 5. Gere um dashboard interativo
portfolio.generate_dashboard("meu_dashboard.html")
print("\n✅ Dashboard criado! Abra 'meu_dashboard.html' no navegador")
```

Execute:
```bash
python quick_start.py
```

## Comandos Essenciais

### Ver Análise Completa
```python
analysis = portfolio.analyze()
print(analysis)
```

### Adicionar Mais Ações
```python
portfolio.add_stock("TSLA", shares=5, purchase_price=240.00)
```

### Vender Ações
```python
current_price = portfolio.stocks["AAPL"].get_current_price()
portfolio.sell_stock("AAPL", shares=3, price=current_price)
```

### Ver Alocação
```python
allocation = portfolio.get_allocation()
for stock, percent in allocation.items():
    print(f"{stock}: {percent:.2f}%")
```

### Salvar/Carregar Portfólio
```python
# Salvar
portfolio.save("meu_portfolio.json")

# Carregar
from src.core import Portfolio
portfolio = Portfolio.load("meu_portfolio.json")
```

## Usando a API REST

### 1. Inicie o servidor
```bash
cd src/api
uvicorn main:app --reload
```

### 2. Acesse a documentação interativa
Abra no navegador: http://localhost:8000/docs

### 3. Exemplos de requisições

**Criar portfólio:**
```bash
curl -X POST "http://localhost:8000/portfolios" \
  -H "Content-Type: application/json" \
  -d '{"name": "Meu Portfolio", "cash": 10000}'
```

**Adicionar ação:**
```bash
curl -X POST "http://localhost:8000/portfolios/portfolio_1/stocks" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "shares": 10, "purchase_price": 150.00}'
```

**Ver análise:**
```bash
curl "http://localhost:8000/portfolios/portfolio_1/analysis"
```

## Métricas Disponíveis

O Portfolio Analyzer calcula automaticamente:

- 📊 **Retorno Total** - Quanto você ganhou/perdeu
- 📈 **Sharpe Ratio** - Retorno ajustado ao risco
- 📉 **Volatilidade** - Quão arriscado é seu portfólio
- 💹 **Beta** - Sensibilidade ao mercado
- ⚠️ **Value at Risk** - Perda máxima esperada
- 📊 **Maximum Drawdown** - Maior queda do pico

## Exemplos Práticos

### Rebalancear Portfólio
```python
# Ver alocação atual
allocation = portfolio.get_allocation()

# Ajustar para ter 40% em cada ação principal
target_value = portfolio.total_value * 0.40

for symbol in ['AAPL', 'GOOGL']:
    stock = portfolio.stocks[symbol]
    current_value = stock.current_value
    
    if current_value < target_value:
        # Comprar mais
        shares_to_buy = (target_value - current_value) / stock.get_current_price()
        portfolio.add_stock(symbol, shares=shares_to_buy, purchase_price=stock.get_current_price())
```

### Monitorar Performance
```python
# Calcular métricas
metrics = portfolio.calculate_metrics(period="1y")

print(f"Retorno Anualizado: {metrics['annualized_return']:.2f}%")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
print(f"Volatilidade: {metrics['volatility']*100:.2f}%")

# Alertas simples
if metrics['sharpe_ratio'] < 1.0:
    print("⚠️ ALERTA: Sharpe Ratio abaixo de 1.0 - considere rebalancear")

if metrics['max_drawdown'] < -20:
    print("⚠️ ALERTA: Drawdown significativo - revisar estratégia")
```

### Diversificação por Setor
```python
sector_allocation = portfolio.get_sector_allocation()

print("\n🏢 Diversificação por Setor:")
for sector, percent in sorted(sector_allocation.items(), key=lambda x: x[1], reverse=True):
    print(f"{sector:20s}: {percent:6.2f}%")

# Verificar concentração
if any(percent > 50 for percent in sector_allocation.values()):
    print("\n⚠️ ALERTA: Mais de 50% em um único setor!")
```

## Próximos Passos

1. 📖 Leia o [README completo](../README.md)
2. 🎯 Execute o [exemplo completo](../examples/basic_usage.py)
3. 🧪 Rode os testes: `pytest`
4. 📚 Consulte a [documentação](../docs/)
5. 🚀 Explore features avançadas

## Recursos Adicionais

- [Documentação da API](../docs/api_reference.md)
- [Exemplos Avançados](../examples/)
- [Testes](../tests/)
- [Contribuindo](../CONTRIBUTING.md)

## Precisa de Ajuda?

- 📧 Email: seu.email@example.com
- 🐛 Issues: https://github.com/seu-usuario/portfolio-analyzer/issues
- 💬 Discussions: https://github.com/seu-usuario/portfolio-analyzer/discussions

---

**Dica**: Comece pequeno! Adicione 2-3 ações, explore o dashboard, e depois expanda gradualmente.

Bom investimento! 📈
