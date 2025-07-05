from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import asyncio
from typing import List
import uvicorn
from datetime import datetime

app = FastAPI(title="Trading Dashboard", version="1.0.0")

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Mock market data for testing (will be replaced with real IBKR data)
mock_market_data = {
    "AAPL": {
        "symbol": "AAPL",
        "price": 150.25,
        "change": 0.75,
        "change_percent": 0.50,
        "volume": 45678901,
        "timestamp": datetime.now().isoformat()
    },
    "TSLA": {
        "symbol": "TSLA", 
        "price": 245.80,
        "change": -2.20,
        "change_percent": -0.89,
        "volume": 23456789,
        "timestamp": datetime.now().isoformat()
    }
}

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stock-card {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .stock-symbol {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .stock-price {
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .stock-change {
                font-size: 18px;
                margin-bottom: 10px;
            }
            .positive { color: #4ade80; }
            .negative { color: #f87171; }
            .status {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                text-align: center;
            }
            .connection-status {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .connected { background: #4ade80; }
            .disconnected { background: #f87171; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Trading Dashboard</h1>
                <p>Real-time market data and trading insights</p>
            </div>
            
            <div class="status">
                <span class="connection-status disconnected" id="connectionStatus"></span>
                <span id="connectionText">Disconnected</span>
            </div>
            
            <div class="dashboard-grid" id="stockGrid">
                <!-- Stock cards will be populated here -->
            </div>
        </div>

        <script>
            const ws = new WebSocket(`ws://${window.location.host}/ws`);
            const stockGrid = document.getElementById('stockGrid');
            const connectionStatus = document.getElementById('connectionStatus');
            const connectionText = document.getElementById('connectionText');

            ws.onopen = function() {
                connectionStatus.className = 'connection-status connected';
                connectionText.textContent = 'Connected - Receiving live data';
            };

            ws.onclose = function() {
                connectionStatus.className = 'connection-status disconnected';
                connectionText.textContent = 'Disconnected';
            };

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateStockCard(data);
            };

            function updateStockCard(stockData) {
                const symbol = stockData.symbol;
                let card = document.getElementById(`card-${symbol}`);
                
                if (!card) {
                    card = createStockCard(stockData);
                    stockGrid.appendChild(card);
                } else {
                    updateStockCardContent(card, stockData);
                }
            }

            function createStockCard(stockData) {
                const card = document.createElement('div');
                card.className = 'stock-card';
                card.id = `card-${stockData.symbol}`;
                updateStockCardContent(card, stockData);
                return card;
            }

            function updateStockCardContent(card, stockData) {
                const changeClass = stockData.change >= 0 ? 'positive' : 'negative';
                const changeSymbol = stockData.change >= 0 ? '+' : '';
                
                card.innerHTML = `
                    <div class="stock-symbol">${stockData.symbol}</div>
                    <div class="stock-price">$${stockData.price.toFixed(2)}</div>
                    <div class="stock-change ${changeClass}">
                        ${changeSymbol}$${stockData.change.toFixed(2)} (${changeSymbol}${stockData.change_percent.toFixed(2)}%)
                    </div>
                    <div>Volume: ${stockData.volume.toLocaleString()}</div>
                    <div style="font-size: 12px; opacity: 0.7;">
                        Last updated: ${new Date(stockData.timestamp).toLocaleTimeString()}
                    </div>
                `;
            }
        </script>
    </body>
    </html>
    """

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial data
        for symbol, data in mock_market_data.items():
            await websocket.send_text(json.dumps(data))
        
        # Keep connection alive and send periodic updates
        while True:
            await asyncio.sleep(2)
            # Simulate price updates
            for symbol in mock_market_data:
                import random
                mock_market_data[symbol]["price"] += random.uniform(-0.50, 0.50)
                mock_market_data[symbol]["change"] = mock_market_data[symbol]["price"] - 150.00
                mock_market_data[symbol]["change_percent"] = (mock_market_data[symbol]["change"] / 150.00) * 100
                mock_market_data[symbol]["timestamp"] = datetime.now().isoformat()
                await websocket.send_text(json.dumps(mock_market_data[symbol]))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/market-data")
async def get_market_data():
    """API endpoint to get current market data"""
    return mock_market_data

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 