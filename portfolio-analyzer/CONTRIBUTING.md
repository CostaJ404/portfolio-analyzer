# Contribuindo para Portfolio Analyzer

Obrigado por considerar contribuir para o Portfolio Analyzer! 🎉

## Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor crie uma issue incluindo:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Versão do Python e dependências
- Logs de erro (se aplicável)

### Sugerindo Melhorias

Sugestões são bem-vindas! Crie uma issue descrevendo:

- O problema que a melhoria resolve
- Como você imagina a solução
- Possíveis alternativas consideradas

### Pull Requests

1. **Fork o repositório**
   ```bash
   git clone https://github.com/seu-usuario/portfolio-analyzer.git
   cd portfolio-analyzer
   ```

2. **Crie um branch para sua feature**
   ```bash
   git checkout -b feature/MinhaNovaFeature
   ```

3. **Configure o ambiente de desenvolvimento**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Faça suas alterações**
   - Escreva código limpo e bem documentado
   - Siga as convenções de estilo Python (PEP 8)
   - Adicione testes para novas funcionalidades
   - Atualize a documentação

5. **Execute os testes**
   ```bash
   # Rode todos os testes
   pytest
   
   # Com cobertura
   pytest --cov=src tests/
   
   # Formatação de código
   black src/ tests/
   
   # Linting
   flake8 src/ tests/
   ```

6. **Commit suas mudanças**
   ```bash
   git add .
   git commit -m "Add: MinhaNovaFeature - descrição breve"
   ```
   
   **Convenção de commits:**
   - `Add:` - Nova funcionalidade
   - `Fix:` - Correção de bug
   - `Update:` - Atualização de funcionalidade existente
   - `Docs:` - Mudanças na documentação
   - `Test:` - Adição ou modificação de testes
   - `Refactor:` - Refatoração de código

7. **Push para o GitHub**
   ```bash
   git push origin feature/MinhaNovaFeature
   ```

8. **Abra um Pull Request**
   - Descreva claramente as mudanças
   - Referencie issues relacionadas
   - Aguarde review

## Padrões de Código

### Python Style Guide

- Siga o PEP 8
- Use type hints quando possível
- Docstrings no formato Google

Exemplo:
```python
def calculate_returns(self, period: str = "1y") -> pd.Series:
    """
    Calcula os retornos diários.
    
    Args:
        period: Período de análise ('1d', '1mo', '1y', etc.)
    
    Returns:
        Series com os retornos diários
    
    Raises:
        ValueError: Se o período for inválido
    """
    pass
```

### Testes

- Escreva testes para todas as novas funcionalidades
- Mantenha cobertura de testes acima de 80%
- Use fixtures do pytest quando apropriado
- Nomeie testes claramente: `test_funcao_comportamento_esperado`

### Documentação

- Atualize o README.md se necessário
- Adicione docstrings em todas as funções/classes públicas
- Crie exemplos de uso para funcionalidades complexas

## Estrutura de Diretórios

```
portfolio-analyzer/
├── src/                    # Código fonte
│   ├── core/              # Lógica principal
│   ├── api/               # API REST
│   ├── dashboard/         # Interface web
│   └── utils/             # Utilitários
├── tests/                 # Testes
├── examples/              # Exemplos de uso
├── docs/                  # Documentação
└── data/                  # Dados e cache
```

## Desenvolvimento Local

### Executando a API

```bash
cd src/api
uvicorn main:app --reload
```

Acesse: http://localhost:8000/docs

### Executando Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_portfolio.py -v

# Com cobertura
pytest --cov=src --cov-report=html
```

### Gerando Documentação

```bash
cd docs
mkdocs serve
```

## Processo de Review

Todas as submissões passam por review. Procuramos:

- ✅ Código limpo e bem documentado
- ✅ Testes adequados
- ✅ Sem quebras de funcionalidades existentes
- ✅ Documentação atualizada
- ✅ Commits bem organizados

## Código de Conduta

### Nossos Valores

- Respeito e inclusão
- Comunicação construtiva
- Colaboração aberta
- Foco em soluções

### Comportamentos Inaceitáveis

- Linguagem ofensiva ou discriminatória
- Ataques pessoais
- Assédio de qualquer tipo
- Compartilhamento de informações privadas

## Dúvidas?

Se tiver dúvidas sobre como contribuir:

- Abra uma issue com a label `question`
- Entre em contato: seu.email@example.com
- Consulte a [documentação](docs/)

## Agradecimentos

Obrigado por contribuir para tornar o Portfolio Analyzer melhor! 🙏

---

**Nota**: Ao contribuir, você concorda que suas contribuições serão licenciadas sob a Licença MIT.
