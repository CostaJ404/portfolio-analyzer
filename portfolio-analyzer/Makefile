.PHONY: help install dev-install test test-cov lint format clean run-api run-example docs

help:
	@echo "Portfolio Analyzer - Comandos Disponíveis"
	@echo ""
	@echo "  make install        - Instala dependências de produção"
	@echo "  make dev-install    - Instala dependências de desenvolvimento"
	@echo "  make test           - Executa testes"
	@echo "  make test-cov       - Executa testes com cobertura"
	@echo "  make lint           - Verifica código com flake8"
	@echo "  make format         - Formata código com black"
	@echo "  make clean          - Remove arquivos temporários"
	@echo "  make run-api        - Inicia servidor API"
	@echo "  make run-example    - Executa exemplo básico"
	@echo "  make docs           - Gera documentação"
	@echo ""

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install -e .
	@echo "✓ Ambiente de desenvolvimento configurado!"

test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html --cov-report=term
	@echo ""
	@echo "✓ Relatório de cobertura gerado em: htmlcov/index.html"

lint:
	flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__
	@echo "✓ Lint concluído!"

format:
	black src/ tests/ examples/ --line-length=100
	isort src/ tests/ examples/
	@echo "✓ Código formatado!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
	rm -f *.html *.json *.log
	@echo "✓ Arquivos temporários removidos!"

run-api:
	cd src/api && uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-example:
	cd examples && python basic_usage.py

docs:
	cd docs && mkdocs build
	@echo "✓ Documentação gerada em: docs/site/"

docker-build:
	docker build -t portfolio-analyzer .

docker-run:
	docker run -p 8000:8000 portfolio-analyzer

setup: dev-install
	@echo ""
	@echo "=========================================="
	@echo "Portfolio Analyzer - Setup Completo!"
	@echo "=========================================="
	@echo ""
	@echo "Próximos passos:"
	@echo "  1. Execute 'make run-example' para testar"
	@echo "  2. Execute 'make run-api' para iniciar a API"
	@echo "  3. Execute 'make test' para rodar os testes"
	@echo ""
