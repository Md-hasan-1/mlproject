from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestionConfig
import sys
from dataclasses import dataclass
import os
import pandas as pd
from src.utils import get_transformer
import numpy as np
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")


@dataclass
class DataTransformation(DataTransformationConfig):
    def initiate_transformation(self):
        try:
            train_df = pd.read_csv(DataIngestionConfig.train_data_path)
            test_df = pd.read_csv(DataIngestionConfig.test_data_path)

            target_column_name = "math_score"

            # creating list of numerical and categorical features
            num_features = [feature for feature in train_df.columns if train_df[feature].dtype != "O" and feature!=target_column_name]
            cat_features = [feature for feature in train_df.columns if train_df[feature].dtype == "O" and feature!=target_column_name]

            # getting preprocessor object
            preprocessor = get_transformer(num_features, cat_features)

            # X(input) features
            X_features_train_df = train_df.drop(target_column_name, axis=1)
            X_features_test_df = test_df.drop(target_column_name, axis=1)

            # processed X(input) features
            X_features_train_arr = preprocessor.fit_transform(X_features_train_df)
            X_features_test_arr = preprocessor.transform(X_features_test_df)

            # saving preprocessor object into a pickle file
            save_object(
                obj=preprocessor,
                file_path=self.preprocessor_path
            )
            logging.info("preprocessor object saved successfully")

            # Merging processed data with output feature
            train_arr = np.c_[
                X_features_train_arr, np.array(train_df[target_column_name])
            ]
            test_arr = np.c_[
                X_features_test_arr, np.array(test_df[target_column_name])
            ]

            return (train_arr, test_arr)
        
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
