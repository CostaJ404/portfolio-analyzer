# 📊 Portfolio Analyzer - Sistema Avançado de Análise de Investimentos

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Um sistema completo de análise de portfólio de investimentos com dashboard interativo, API REST, otimização de carteira e backtesting.

## ✨ Features

- 📈 **Análise em Tempo Real**: Obtenha dados atualizados de ações via API Yahoo Finance
- 📊 **Dashboard Interativo**: Visualize seu portfólio com gráficos interativos (Plotly)
- 🎯 **Otimização de Portfólio**: Encontre a alocação ótima usando Teoria Moderna de Portfólio
- 📉 **Análise de Risco**: Calcule métricas como Sharpe Ratio, Beta, Volatilidade, VaR
- 🔄 **Backtesting**: Teste estratégias de investimento com dados históricos
- 🚀 **API REST**: FastAPI para integração com outros sistemas
- 📱 **Reports PDF**: Gere relatórios profissionais em PDF
- 🔔 **Alertas**: Sistema de notificações para metas e limites
- 💾 **Cache Inteligente**: Otimização de performance com cache de dados
- 🧪 **Testes Completos**: Cobertura de testes com pytest

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/portfolio-analyzer.git
cd portfolio-analyzer

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Uso Básico

```python
from portfolio_analyzer import Portfolio, Stock

# Crie um portfólio
portfolio = Portfolio(name="Meu Portfólio")

# Adicione ações
portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
portfolio.add_stock("GOOGL", shares=5, purchase_price=2800.00)
portfolio.add_stock("MSFT", shares=15, purchase_price=300.00)

# Análise completa
analysis = portfolio.analyze()
print(f"Valor Total: ${analysis['total_value']:,.2f}")
print(f"Retorno: {analysis['total_return']:.2f}%")
print(f"Sharpe Ratio: {analysis['sharpe_ratio']:.3f}")

# Gere o dashboard
portfolio.generate_dashboard(output_file="dashboard.html")
```

### API REST

```bash
# Inicie o servidor
python -m uvicorn src.api.main:app --reload

# Acesse a documentação interativa
# http://localhost:8000/docs
```

### Dashboard Web

```bash
# Execute o dashboard Streamlit
streamlit run src/dashboard/app.py
```

## 📁 Estrutura do Projeto

```
portfolio-analyzer/
├── src/
│   ├── core/
│   │   ├── portfolio.py      # Classe principal do portfólio
│   │   ├── stock.py          # Gerenciamento de ações
│   │   ├── analyzer.py       # Análise financeira
│   │   └── optimizer.py      # Otimização de carteira
│   ├── api/
│   │   ├── main.py           # FastAPI application
│   │   └── routes/           # Endpoints da API
│   ├── dashboard/
│   │   ├── app.py            # Streamlit dashboard
│   │   └── components/       # Componentes visuais
│   ├── utils/
│   │   ├── data_fetcher.py   # Obtenção de dados
│   │   ├── metrics.py        # Cálculo de métricas
│   │   └── cache.py          # Sistema de cache
│   └── reports/
│       └── pdf_generator.py  # Geração de relatórios
├── tests/                     # Testes unitários
├── data/                      # Dados e cache
├── docs/                      # Documentação
├── examples/                  # Exemplos de uso
├── requirements.txt
├── setup.py
└── README.md
```

## 📊 Métricas Calculadas

- **Retorno Total**: Ganho/perda percentual
- **Sharpe Ratio**: Retorno ajustado ao risco
- **Volatilidade**: Desvio padrão dos retornos
- **Beta**: Sensibilidade ao mercado
- **Alpha**: Retorno excedente
- **Value at Risk (VaR)**: Perda máxima esperada
- **Maximum Drawdown**: Maior queda do pico
- **Correlation Matrix**: Correlação entre ativos

## 🎯 Exemplos Avançados

### Otimização de Portfólio

```python
from portfolio_analyzer import PortfolioOptimizer

# Otimize seu portfólio
optimizer = PortfolioOptimizer(portfolio)
optimal_weights = optimizer.optimize(
    objective='sharpe',  # max sharpe ratio
    constraints={'min_weight': 0.05, 'max_weight': 0.40}
)

print("Alocação Ótima:")
for stock, weight in optimal_weights.items():
    print(f"{stock}: {weight*100:.2f}%")
```

### Backtesting

```python
from portfolio_analyzer import Backtester

# Teste uma estratégia
backtester = Backtester(portfolio)
results = backtester.run(
    start_date='2020-01-01',
    end_date='2023-12-31',
    rebalance_frequency='quarterly'
)

print(f"Retorno Total: {results['total_return']:.2f}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.3f}")
```

### Geração de Relatório

```python
from portfolio_analyzer import ReportGenerator

# Gere um relatório PDF profissional
generator = ReportGenerator(portfolio)
generator.create_report(
    output_file='relatorio_portfolio.pdf',
    include_charts=True,
    include_recommendations=True
)
```

## 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
# APIs (opcional - usa dados gratuitos por padrão)
ALPHA_VANTAGE_KEY=your_key_here
POLYGON_API_KEY=your_key_here

# Configurações
CACHE_ENABLED=true
CACHE_TTL=3600
LOG_LEVEL=INFO
```

## 📚 Documentação

Para documentação completa, visite [docs/](docs/)

- [Guia do Usuário](docs/user_guide.md)
- [Referência da API](docs/api_reference.md)
- [Guia de Desenvolvimento](docs/development.md)

## 🧪 Testes

```bash
# Execute todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Testes específicos
pytest tests/test_portfolio.py -v
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 License

Este projeto está licenciado sob a Licença MIT - veja [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Seu Nome - @CostaJ404

## 🙏 Agradecimentos

- [yfinance](https://github.com/ranaroussi/yfinance) - Dados financeiros
- [Plotly](https://plotly.com/) - Visualizações interativas
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
- [Streamlit](https://streamlit.io/) - Dashboard

## 📈 Roadmap

- [ ] Integração com mais exchanges
- [ ] Análise de criptomoedas
- [ ] Machine Learning para previsões
- [ ] Mobile app
- [ ] Trading automatizado
- [ ] Análise de notícias e sentiment

