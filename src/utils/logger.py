import logging
import sys

def setup_logger():
    """Configures and returns a logger to write to file and console."""
    logger = logging.getLogger("BinanceBot")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

   
    file_handler = logging.FileHandler("bot.log")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

   
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_formatter = logging.Formatter("%(levelname)s: %(message)s")
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger


log = setup_logger() 