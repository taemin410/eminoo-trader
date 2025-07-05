# 🚀 Eminoo Trader

> **Algorithmic Trading Platform with Interactive Brokers Integration**

A Python-based trading system for real-time market data, streaming, and automated strategies using Interactive Brokers API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![IBKR](https://img.shields.io/badge/Interactive%20Brokers-API-orange.svg)

## ✨ Features

- 🔌 **IBKR Integration** - Connect to Interactive Brokers Gateway/TWS
- 📊 **Real-time Data** - Live streaming of stock prices, bid/ask, volume
- 🔄 **Streaming** - Continuous data feeds with custom callbacks
- 💾 **Data Persistence** - Save market data to JSON files
- 📈 **Account Management** - View account summaries

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Interactive Brokers account
- IB Gateway/TWS running with API enabled

### Installation

```bash
git clone https://github.com/yourusername/eminoo-trader.git
cd eminoo-trader
pip install -r requirements.txt
```

### Basic Usage

```python
from algotrader.ibkr_client import IBKRClient

client = IBKRClient()
client.connect()
data = client.request_market_data('AAPL')
print(f"AAPL: ${data['last']:.2f}")
client.disconnect()
```

## 📊 Examples

**Basic market data:**

```bash
python main.py
```

**Advanced streaming:**

```bash
python streaming_example.py
```

### Streaming with Callbacks

```python
def my_handler(data):
    print(f"🔄 {data['symbol']}: ${data['last']:.2f}")

client.start_streaming_market_data('AAPL', callback=my_handler)
```

## 🔧 Configuration

**Connection settings:**

```python
# Paper trading (default)
client = IBKRClient(host='127.0.0.1', port=4002)

# Live trading
client = IBKRClient(host='127.0.0.1', port=7497)
```

## 📚 Dependencies

- **ib-insync** - Interactive Brokers Python API wrapper

## ⚠️ Disclaimer

For educational purposes only. Trading involves risk of loss.

---

**Made with ❤️ for algorithmic traders**
