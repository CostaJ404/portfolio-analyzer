"""
API REST para Portfolio Analyzer usando FastAPI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import sys
sys.path.insert(0, '../../src')

from core import Portfolio, Stock

# Modelos Pydantic
class StockInput(BaseModel):
    symbol: str
    shares: float
    purchase_price: float
    name: Optional[str] = None

class PortfolioCreate(BaseModel):
    name: str
    cash: float = 0

class SellStockInput(BaseModel):
    symbol: str
    shares: float
    price: float

# Inicialização
app = FastAPI(
    title="Portfolio Analyzer API",
    description="API REST para análise de portfólio de investimentos",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Armazenamento em memória (em produção, usar banco de dados)
portfolios: Dict[str, Portfolio] = {}

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Portfolio Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "portfolios_count": len(portfolios)
    }

@app.post("/portfolios", status_code=201)
async def create_portfolio(portfolio_data: PortfolioCreate):
    """Cria um novo portfólio"""
    portfolio_id = f"portfolio_{len(portfolios) + 1}"
    portfolio = Portfolio(name=portfolio_data.name, cash=portfolio_data.cash)
    portfolios[portfolio_id] = portfolio
    
    return {
        "portfolio_id": portfolio_id,
        "name": portfolio.name,
        "cash": portfolio.cash,
        "created_at": portfolio.creation_date.isoformat()
    }

@app.get("/portfolios")
async def list_portfolios():
    """Lista todos os portfólios"""
    return {
        "portfolios": [
            {
                "id": pid,
                "name": p.name,
                "total_value": p.total_value,
                "num_stocks": len(p.stocks)
            }
            for pid, p in portfolios.items()
        ]
    }

@app.get("/portfolios/{portfolio_id}")
async def get_portfolio(portfolio_id: str):
    """Obtém detalhes de um portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    portfolio = portfolios[portfolio_id]
    return {
        "id": portfolio_id,
        "name": portfolio.name,
        "total_value": portfolio.total_value,
        "total_invested": portfolio.total_invested,
        "total_return": portfolio.total_return,
        "cash": portfolio.cash,
        "stocks": [
            {
                "symbol": symbol,
                "shares": stock.shares,
                "current_value": stock.current_value
            }
            for symbol, stock in portfolio.stocks.items()
        ]
    }

@app.post("/portfolios/{portfolio_id}/stocks")
async def add_stock_to_portfolio(portfolio_id: str, stock_data: StockInput):
    """Adiciona uma ação ao portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    portfolio = portfolios[portfolio_id]
    portfolio.add_stock(
        symbol=stock_data.symbol,
        shares=stock_data.shares,
        purchase_price=stock_data.purchase_price,
        name=stock_data.name
    )
    
    return {
        "message": f"Ação {stock_data.symbol} adicionada com sucesso",
        "symbol": stock_data.symbol,
        "shares": stock_data.shares,
        "purchase_price": stock_data.purchase_price
    }

@app.delete("/portfolios/{portfolio_id}/stocks/{symbol}")
async def remove_stock_from_portfolio(portfolio_id: str, symbol: str):
    """Remove uma ação do portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    portfolio = portfolios[portfolio_id]
    symbol = symbol.upper()
    
    if symbol not in portfolio.stocks:
        raise HTTPException(status_code=404, detail="Ação não encontrada no portfólio")
    
    portfolio.remove_stock(symbol)
    
    return {"message": f"Ação {symbol} removida com sucesso"}

@app.post("/portfolios/{portfolio_id}/sell")
async def sell_stock(portfolio_id: str, sell_data: SellStockInput):
    """Vende ações de um portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    portfolio = portfolios[portfolio_id]
    
    try:
        portfolio.sell_stock(
            symbol=sell_data.symbol,
            shares=sell_data.shares,
            price=sell_data.price
        )
        return {
            "message": f"Vendidas {sell_data.shares} ações de {sell_data.symbol}",
            "total_received": sell_data.shares * sell_data.price,
            "new_cash_balance": portfolio.cash
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/portfolios/{portfolio_id}/analysis")
async def analyze_portfolio(portfolio_id: str, period: str = "1y"):
    """Retorna análise completa do portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    portfolio = portfolios[portfolio_id]
    analysis = portfolio.analyze(period=period)
    
    return analysis

@app.get("/portfolios/{portfolio_id}/metrics")
async def get_portfolio_metrics(portfolio_id: str, period: str = "1y"):
    """Retorna métricas de performance do portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    portfolio = portfolios[portfolio_id]
    metrics = portfolio.calculate_metrics(period=period)
    
    return metrics

@app.get("/portfolios/{portfolio_id}/allocation")
async def get_portfolio_allocation(portfolio_id: str):
    """Retorna a alocação do portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    portfolio = portfolios[portfolio_id]
    
    return {
        "stock_allocation": portfolio.get_allocation(),
        "sector_allocation": portfolio.get_sector_allocation()
    }

@app.get("/stocks/{symbol}")
async def get_stock_info(symbol: str):
    """Obtém informações sobre uma ação específica"""
    try:
        stock = Stock(symbol=symbol)
        current_price = stock.get_current_price()
        info = stock.get_info()
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "name": info.get('longName', symbol),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": info.get('marketCap', 0),
            "pe_ratio": info.get('trailingPE', 0),
            "dividend_yield": info.get('dividendYield', 0),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao obter informações: {str(e)}")

@app.get("/stocks/{symbol}/history")
async def get_stock_history(
    symbol: str,
    period: str = "1y",
    interval: str = "1d"
):
    """Obtém histórico de preços de uma ação"""
    try:
        stock = Stock(symbol=symbol)
        history = stock.get_historical_data(period=period, interval=interval)
        
        if history.empty:
            return {"data": []}
        
        return {
            "symbol": symbol,
            "period": period,
            "interval": interval,
            "data": [
                {
                    "date": idx.isoformat(),
                    "open": row['Open'],
                    "high": row['High'],
                    "low": row['Low'],
                    "close": row['Close'],
                    "volume": row['Volume']
                }
                for idx, row in history.iterrows()
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao obter histórico: {str(e)}")

@app.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(portfolio_id: str):
    """Deleta um portfólio"""
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail="Portfólio não encontrado")
    
    del portfolios[portfolio_id]
    return {"message": "Portfólio deletado com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
