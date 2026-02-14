# 🎯 GUIA COMPLETO - Portfolio Analyzer

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Estrutura do Projeto](#estrutura)
4. [Como Usar](#como-usar)
5. [Recursos Avançados](#recursos-avançados)
6. [Desenvolvimento](#desenvolvimento)
7. [Deploy](#deploy)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O **Portfolio Analyzer** é um sistema completo e profissional de análise de portfólio de investimentos que inclui:

### Features Principais
- ✅ Análise de ações em tempo real (Yahoo Finance)
- ✅ Cálculo de métricas financeiras avançadas
- ✅ Dashboard interativo com Plotly
- ✅ API REST com FastAPI
- ✅ Otimização de carteira (Teoria Moderna de Portfólio)
- ✅ Sistema de testes completo
- ✅ CI/CD com GitHub Actions
- ✅ Documentação completa

### Tecnologias Utilizadas
- **Backend**: Python 3.9+
- **Dados**: yfinance, pandas, numpy
- **Visualização**: Plotly, Matplotlib
- **API**: FastAPI, Uvicorn
- **Testes**: Pytest
- **CI/CD**: GitHub Actions

---

## 🚀 Instalação

### Pré-requisitos
```bash
# Python 3.9 ou superior
python --version

# Git
git --version
```

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/portfolio-analyzer.git
cd portfolio-analyzer

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Instale o pacote em modo desenvolvimento
pip install -e .

# 6. Configure as variáveis de ambiente (opcional)
cp .env.example .env
# Edite .env conforme necessário

# 7. Verifique a instalação
python -c "from src.core import Portfolio; print('✓ Instalação OK!')"
```

### Instalação Rápida com Make
```bash
make setup
```

---

## 📁 Estrutura do Projeto

```
portfolio-analyzer/
│
├── src/                          # Código fonte
│   ├── core/                     # Lógica principal
│   │   ├── __init__.py
│   │   ├── portfolio.py         # Classe Portfolio
│   │   └── stock.py             # Classe Stock
│   │
│   ├── api/                      # API REST
│   │   └── main.py              # FastAPI app
│   │
│   └── __init__.py
│
├── tests/                        # Testes
│   └── test_portfolio.py
│
├── examples/                     # Exemplos
│   ├── basic_usage.py           # Uso básico
│   └── advanced_optimization.py # Otimização avançada
│
├── docs/                         # Documentação
│   └── QUICKSTART.md
│
├── .github/                      # GitHub Actions
│   └── workflows/
│       └── ci.yml
│
├── data/                         # Dados e cache
├── logs/                         # Logs
│
├── requirements.txt              # Dependências
├── setup.py                      # Configuração do pacote
├── pytest.ini                    # Configuração pytest
├── Makefile                      # Comandos úteis
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

---

## 💻 Como Usar

### 1. Uso Básico

```python
from src.core import Portfolio

# Criar portfólio
portfolio = Portfolio(name="Meu Portfólio", cash=10000)

# Adicionar ações
portfolio.add_stock("AAPL", shares=10, purchase_price=150.00)
portfolio.add_stock("GOOGL", shares=5, purchase_price=140.00)
portfolio.add_stock("MSFT", shares=15, purchase_price=380.00)

# Ver resumo
print(portfolio)

# Análise completa
analysis = portfolio.analyze()
print(f"Valor Total: ${analysis['total_value']:,.2f}")
print(f"Retorno: {analysis['total_return']:.2f}%")

# Gerar dashboard
portfolio.generate_dashboard("dashboard.html")

# Salvar portfólio
portfolio.save("meu_portfolio.json")
```

### 2. Executar Exemplos

```bash
# Exemplo básico
cd examples
python basic_usage.py

# Exemplo avançado (otimização)
python advanced_optimization.py
```

### 3. Usar a API REST

```bash
# Iniciar servidor
cd src/api
uvicorn main:app --reload

# Ou usando Make
make run-api
```

Acesse: http://localhost:8000/docs

#### Exemplos de Endpoints:

```bash
# Criar portfólio
curl -X POST "http://localhost:8000/portfolios" \
  -H "Content-Type: application/json" \
  -d '{"name": "Meu Portfolio", "cash": 10000}'

# Adicionar ação
curl -X POST "http://localhost:8000/portfolios/portfolio_1/stocks" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "shares": 10, "purchase_price": 150.00}'

# Ver análise
curl "http://localhost:8000/portfolios/portfolio_1/analysis"
```

### 4. Rodar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Ou usando Make
make test
make test-cov
```

---

## 🎓 Recursos Avançados

### Otimização de Portfólio

```python
from examples.advanced_optimization import PortfolioOptimizer

optimizer = PortfolioOptimizer(portfolio)
optimizer.prepare_data(period="1y")

# Maximizar Sharpe Ratio
optimal_weights = optimizer.optimize_sharpe_ratio()

# Minimizar Risco
min_risk_weights = optimizer.optimize_min_variance()

# Retorno Alvo
target_weights = optimizer.optimize_target_return(target_return=0.15)
```

### Métricas Disponíveis

```python
metrics = portfolio.calculate_metrics(period="1y")

print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
print(f"Volatilidade: {metrics['volatility']*100:.2f}%")
print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
print(f"VaR (95%): {metrics['var_95']:.2f}%")
```

### Análise de Correlação

```python
corr_matrix = portfolio.calculate_correlation_matrix()
print(corr_matrix)
```

### Alocação por Setor

```python
sector_allocation = portfolio.get_sector_allocation()
for sector, percent in sector_allocation.items():
    print(f"{sector}: {percent:.2f}%")
```

---

## 🛠️ Desenvolvimento

### Setup do Ambiente de Desenvolvimento

```bash
# Instalar dependências de dev
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Ou
make dev-install
```

### Comandos Úteis

```bash
# Formatar código
make format

# Verificar estilo
make lint

# Rodar testes
make test

# Limpar arquivos temporários
make clean
```

### Adicionar Novas Features

1. Crie um branch
```bash
git checkout -b feature/nova-feature
```

2. Faça as alterações

3. Adicione testes
```python
# Em tests/test_portfolio.py
def test_nova_feature():
    # Seu teste aqui
    pass
```

4. Execute os testes
```bash
pytest
```

5. Commit e push
```bash
git add .
git commit -m "Add: Nova feature"
git push origin feature/nova-feature
```

6. Abra Pull Request

---

## 🚢 Deploy

### Deploy Local

```bash
# API
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Deploy com Docker (Futuro)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t portfolio-analyzer .
docker run -p 8000:8000 portfolio-analyzer
```

### Deploy na Cloud

#### Heroku
```bash
# Criar Procfile
echo "web: uvicorn src.api.main:app --host 0.0.0.0 --port \$PORT" > Procfile

heroku create seu-app
git push heroku main
```

#### Railway.app
1. Conecte seu repositório GitHub
2. Configure variáveis de ambiente
3. Deploy automático

---

## 🔧 Troubleshooting

### Erro: ModuleNotFoundError

```bash
# Reinstale o pacote
pip install -e .
```

### Erro ao obter dados de ações

```python
# Verifique conexão com internet
# Tente outro símbolo
# Limpe o cache
```

### Testes falhando

```bash
# Limpe cache do pytest
pytest --cache-clear

# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Performance lenta

```python
# Ative cache
# Em .env:
CACHE_ENABLED=true
CACHE_TTL=3600
```

---

## 📊 Próximos Passos

1. ✅ Clone e configure o projeto
2. ✅ Execute o exemplo básico
3. ✅ Teste a API
4. ✅ Crie seu próprio portfólio
5. ✅ Explore otimizações
6. ✅ Contribua com melhorias

---

## 🤝 Suporte

- 📖 [Documentação](docs/)
- 🐛 [Issues](https://github.com/seu-usuario/portfolio-analyzer/issues)
- 💬 [Discussions](https://github.com/seu-usuario/portfolio-analyzer/discussions)
- 📧 Email: seu.email@example.com

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE)

---

**Desenvolvido com ❤️ para a comunidade de investidores**
