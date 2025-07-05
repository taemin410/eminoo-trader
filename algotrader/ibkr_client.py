from ib_insync import IB, Stock, Contract
import time
from datetime import datetime
import json

class IBKRClient:
    def __init__(self, host='127.0.0.1', port=4002, client_id=1):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()
        self.streaming_data = {}
        self.data_callbacks = []

    def connect(self):
        """Connect to IBKR Gateway/TWS"""
        self.ib.connect(self.host, self.port, self.client_id)
        print(f"Connected to IBKR at {self.host}:{self.port} (clientId={self.client_id})")

    def disconnect(self):
        """Disconnect from IBKR"""
        self.ib.disconnect()
        print("Disconnected from IBKR.")

    def get_stock_contract(self, symbol, exchange='SMART', currency='USD'):
        """Create a stock contract for the given symbol"""
        contract = Stock(symbol, exchange, currency)
        return contract

    def request_market_data(self, symbol, exchange='SMART', currency='USD'):
        """Request real-time market data for a stock"""
        contract = self.get_stock_contract(symbol, exchange, currency)
        
        # Request market data
        self.ib.reqMktData(contract)
        print(f"Requested market data for {symbol}")
        
        # Wait a moment for data to arrive
        self.ib.sleep(1)
        
        # Get the latest tick data
        ticker = self.ib.ticker(contract)
        if ticker:
            return {
                'symbol': symbol,
                'bid': ticker.bid,
                'ask': ticker.ask,
                'last': ticker.last,
                'close': ticker.close,
                'volume': ticker.volume,
                'high': ticker.high,
                'low': ticker.low
            }
        return None

    def start_streaming_market_data(self, symbol, exchange='SMART', currency='USD', callback=None):
        """Start streaming market data with real-time updates"""
        contract = self.get_stock_contract(symbol, exchange, currency)
        
        # Store callback for this symbol
        if callback:
            self.data_callbacks.append((symbol, callback))
        
        # Set up the ticker callback
        def on_ticker_update(ticker):
            if ticker.contract.symbol == symbol:
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'bid': ticker.bid,
                    'ask': ticker.ask,
                    'last': ticker.last,
                    'close': ticker.close,
                    'volume': ticker.volume,
                    'high': ticker.high,
                    'low': ticker.low,
                    'bid_size': ticker.bidSize,
                    'ask_size': ticker.askSize
                }
                
                # Store latest data
                self.streaming_data[symbol] = data
                
                # Call user callback if provided
                if callback:
                    callback(data)
                
                print(f"📊 {symbol}: ${data['last']:.2f} (Bid: ${data['bid']:.2f}, Ask: ${data['ask']:.2f})")
        
        # Register the callback
        self.ib.pendingTickersEvent += on_ticker_update
        
        # Request market data
        self.ib.reqMktData(contract)
        print(f"Started streaming market data for {symbol}")

    def stop_streaming_market_data(self, symbol, exchange='SMART', currency='USD'):
        """Stop streaming market data for a symbol"""
        contract = self.get_stock_contract(symbol, exchange, currency)
        self.ib.cancelMktData(contract)
        
        # Remove from streaming data
        if symbol in self.streaming_data:
            del self.streaming_data[symbol]
        
        # Remove callbacks for this symbol
        self.data_callbacks = [(s, cb) for s, cb in self.data_callbacks if s != symbol]
        
        print(f"Stopped streaming market data for {symbol}")

    def get_latest_data(self, symbol):
        """Get the latest streaming data for a symbol"""
        return self.streaming_data.get(symbol)

    def save_data_to_file(self, symbol, filename=None):
        """Save streaming data to a JSON file"""
        if filename is None:
            filename = f"{symbol}_market_data.json"
        
        data = self.streaming_data.get(symbol)
        if data:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {symbol} data to {filename}")

    def cancel_market_data(self, symbol, exchange='SMART', currency='USD'):
        """Cancel market data subscription for a symbol"""
        contract = self.get_stock_contract(symbol, exchange, currency)
        self.ib.cancelMktData(contract)
        print(f"Cancelled market data for {symbol}")

    def get_account_summary(self):
        """Get account summary information"""
        if not self.ib.isConnected():
            print("Not connected to IBKR")
            return None
        
        # Request account summary
        self.ib.reqAccountSummary(9001, "All", "NetLiquidation")
        self.ib.sleep(1)
        
        # Get account values
        account_values = self.ib.accountSummary()
        return account_values
