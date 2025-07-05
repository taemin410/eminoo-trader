from algotrader.ibkr_client import IBKRClient
import time

def main():
    # Create client instance
    client = IBKRClient()
    
    try:
        # Connect to IBKR
        print("Connecting to IBKR...")
        client.connect()
        
        # Wait a moment for connection to stabilize
        time.sleep(2)
        
        # Request market data for AAPL
        print("\nRequesting market data for AAPL...")
        aapl_data = client.request_market_data('AAPL')
        
        if aapl_data:
            print("\nAAPL Market Data:")
            print(f"Symbol: {aapl_data['symbol']}")
            print(f"Bid: ${aapl_data['bid']:.2f}" if aapl_data['bid'] else "Bid: N/A")
            print(f"Ask: ${aapl_data['ask']:.2f}" if aapl_data['ask'] else "Ask: N/A")
            print(f"Last: ${aapl_data['last']:.2f}" if aapl_data['last'] else "Last: N/A")
            print(f"Close: ${aapl_data['close']:.2f}" if aapl_data['close'] else "Close: N/A")
            print(f"Volume: {aapl_data['volume']:,}" if aapl_data['volume'] else "Volume: N/A")
            print(f"High: ${aapl_data['high']:.2f}" if aapl_data['high'] else "High: N/A")
            print(f"Low: ${aapl_data['low']:.2f}" if aapl_data['low'] else "Low: N/A")
        else:
            print("No market data received for AAPL")
        
        # Get account summary (if connected to live account)
        print("\nRequesting account summary...")
        account_summary = client.get_account_summary()
        if account_summary:
            print("Account Summary:")
            for summary in account_summary:
                print(f"  {summary.tag}: {summary.value}")
        else:
            print("No account summary available (paper trading or not connected)")
        
        # Cancel market data subscription
        client.cancel_market_data('AAPL')
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure IB Gateway/TWS is running and API access is enabled")
    
    finally:
        # Always disconnect
        print("\nDisconnecting...")
        client.disconnect()

if __name__ == "__main__":
    main()
