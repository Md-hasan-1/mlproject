import logging
import os
from datetime import datetime


file_name = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
file_path = os.path.join(os.getcwd(),"logs")

os.makedirs(file_path, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(file_path, file_name),
    datefmt='%Y-%m-%d,%H:%M:%S',
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
    level=logging.DEBUG
)
