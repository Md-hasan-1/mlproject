import pandas as pd
import os
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import sys
from src.utils import get_splits


@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join("artifacts", "data.csv")
    train_data_path = os.path.join("artifacts", "train.csv")
    test_data_path = os.path.join("artifacts", "test.csv")



@dataclass
class DataIngestion(DataIngestionConfig):
    def initiate_ingestion(self):
        try:
            logging.info("Data collection initiated.")
            data_path = os.path.join("data", "StudentPerformance.csv")

            df = pd.read_csv(data_path)
            logging.info("Data collection sucessfully completed.")

            logging.info("Creating splits of train and test")
            train_df, test_df = get_splits(df)
            logging.info("split successfully created")

            # making directory named artifacts to save data
            os.makedirs(os.path.dirname(self.raw_data_path), exist_ok=True)

            # saving row data
            df.to_csv(self.raw_data_path, index=False)
            logging.info("Raw Data saved sucessfully")

            # saving train and test data
            train_df.to_csv(self.train_data_path, index=False)
            logging.info("Train Data saved sucessfully")
            test_df.to_csv(self.test_data_path, index=False)
            logging.info("Test Data saved sucessfully")

            return None
        
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
