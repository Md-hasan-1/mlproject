import pandas as pd
from typing import ClassVar
from src.logger import logging
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.model_selection import train_test_split
import sys
import os


@dataclass
class DataingestionConfig():
    raw_data_path: ClassVar[str] = os.path.join("artifacts", "data.csv")
    train_path: ClassVar[str] = os.path.join("artifacts", "train.csv")
    test_path: ClassVar[str] = os.path.join("artifacts", "test.csv")


@dataclass
class Dataingestion(DataingestionConfig):
    def initiate(self):
        try: 
            # entry log
            logging.info("Data ingestion initiated.")

            # data collection initiated
            logging.info("Data collection initiated.")
            df = pd.read_csv(os.path.join("notebook/data/StudentPerformance.csv"))
            logging.info("Data collection successfully completed.")

            # creating directory to save files
            os.makedirs(os.path.dirname(Dataingestion.raw_data_path), exist_ok=True)

            # saving data into local machine
            df.to_csv(Dataingestion.raw_data_path)
            logging.info("Raw data saved successfully.")

            # train-test-split initiated
            logging.info("train-test-split initiated.")
            train_data, test_data = train_test_split(df, test_size=0.33, random_state=42)
            logging.info("train-test-split successfully exicuted.")

            # saving train data to local machine
            train_data.to_csv(Dataingestion.train_path)
            logging.info("training data saved successfully.")
            
            # saving test data to local machine
            test_data.to_csv(Dataingestion.test_path)
            logging.info("test data saved successfully.")

            # out log
            logging.info("Data ingestion successfully executed.")
            return None

        except Exception as e:
            logging.info(e)
            return CustomException(e, sys)
