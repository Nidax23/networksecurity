import logging
import os

LOG_FILE = "networksecurity.log"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE)),
        logging.StreamHandler()   # 👈 THIS IS REQUIRED
    ]
)

logging = logging.getLogger()
