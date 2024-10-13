import logging
from datetime import datetime
import os


file_name = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
file_folder_path = os.path.join(os.getcwd(), "logs", file_name.split(".")[0])
os.makedirs(file_folder_path, exist_ok=True)

file_path = os.path.join(file_folder_path, file_name)

logging.basicConfig(
    filename=file_path,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[ %(asctime)s ] %(lineno)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
