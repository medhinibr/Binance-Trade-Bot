import argparse
import time
import sys
import os

# Add parent directory to path so we can import config/logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_exchange
from utils.logger import setup_logger

logger = setup_logger()

def execute_twap(symbol, side, total_amount, duration, chunks):
    exchange = get_exchange()
    
    try:
        if total_amount <= 0 or duration <= 0 or chunks <= 0:
            raise ValueError("All numerical inputs must be positive.")

        chunk_size = total_amount / chunks
        interval = duration / chunks  # Seconds between trades

        logger.info(f"Starting TWAP: {side} {total_amount} {symbol} over {duration}s in {chunks} chunks.")
        logger.info(f"Each chunk: {chunk_size} {symbol} every {interval} seconds.")

        for i in range(chunks):
            logger.info(f"Executing TWAP Chunk {i+1}/{chunks}...")
            
            # Execute market order for the chunk
            order = exchange.create_order(
                symbol=symbol,
                type='market',
                side=side.lower(),
                amount=chunk_size
            )
            
            logger.info(f"Chunk {i+1} filled. Price: {order['average'] if 'average' in order else 'Market'}")
            
            if i < chunks - 1:
                time.sleep(interval)
        
        logger.info("TWAP Strategy Completed Successfully.")

    except Exception as e:
        logger.error(f"TWAP Failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute TWAP Strategy")
    parser.add_argument("symbol", type=str)
    parser.add_argument("side", type=str)
    parser.add_argument("total_amount", type=float, help="Total quantity to trade")
    parser.add_argument("duration", type=int, help="Total duration in seconds")
    parser.add_argument("chunks", type=int, help="Number of splits")

    args = parser.parse_args()
    execute_twap(args.symbol, args.side, args.total_amount, args.duration, args.chunks)