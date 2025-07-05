from algotrader.ibkr_client import IBKRClient
import time
import json
from datetime import datetime

def custom_data_handler(data):
    """Custom callback function for processing streaming data"""
    # You can add your custom logic here
    # For example: save to database, trigger alerts, etc.
    print(f"🔄 Custom handler: {data['symbol']} at ${data['last']:.2f}")

def save_to_file_handler(data):
    """Callback that saves data to a file"""
    filename = f"{data['symbol']}_streaming_data.jsonl"
    with open(filename, 'a') as f:
        f.write(json.dumps(data) + '\n')

def main():
    client = IBKRClient()
    
    try:
        print("Connecting to IBKR...")
        client.connect()
        time.sleep(2)
        
        # Start streaming AAPL with custom callback
        print("\nStarting AAPL streaming...")
        client.start_streaming_market_data('AAPL', callback=custom_data_handler)
        
        # Start streaming TSLA with file saving callback
        print("\nStarting TSLA streaming with file saving...")
        client.start_streaming_market_data('TSLA', callback=save_to_file_handler)
        
        # Stream for 30 seconds
        print("\nStreaming for 30 seconds... (Press Ctrl+C to stop early)")
        start_time = time.time()
        
        while time.time() - start_time < 30:
            time.sleep(1)
            
            # You can access latest data anytime
            aapl_data = client.get_latest_data('AAPL')
            if aapl_data:
                print(f"📈 Latest AAPL: ${aapl_data['last']:.2f}")
        
        # Stop streaming
        client.stop_streaming_market_data('AAPL')
        client.stop_streaming_market_data('TSLA')
        
        # Save final data snapshot
        client.save_data_to_file('AAPL', 'aapl_final_snapshot.json')
        
    except KeyboardInterrupt:
        print("\nStopping streams...")
        client.stop_streaming_market_data('AAPL')
        client.stop_streaming_market_data('TSLA')
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        print("Disconnecting...")
        client.disconnect()

if __name__ == "__main__":
    main() 