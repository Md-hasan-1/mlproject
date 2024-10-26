from dataclasses import dataclass
from src.exception import CustomException
import sys
from src.logger import logging
from src.utils import load_object
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig


@dataclass
class Prediction:
    def predict(self, data):
        try:
            preprocessor = load_object(DataTransformationConfig.preprocessor_path)
            model = load_object(ModelTrainerConfig.model_path)
            processed_data = preprocessor.transform(data)
            pred = model.predict(processed_data)
            return pred
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)

