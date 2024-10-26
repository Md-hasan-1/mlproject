from src.exception import CustomException
from src.logger import logging
import sys
import os
from src.components.data_transformation import DataTransformation
from dataclasses import dataclass
from src.utils import get_best_model, save_object

from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor


@dataclass
class ModelTrainerConfig:
    model_path = os.path.join("artifacts", "model.pkl")


@dataclass
class ModelTrainer(ModelTrainerConfig):
    def initiate_training(self):
        try:
            dt = DataTransformation()
            train_arr, test_arr = dt.initiate_transformation()
            X_train, X_test, y_train, y_test = (
                train_arr[:, :-1], # X_train
                test_arr[:, :-1], # X_test
                train_arr[:, -1], # y_train
                test_arr[:, -1] # y_test
            )
            # models
            models = {
                "Random Forest": RandomForestRegressor(n_jobs=-1),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(n_jobs=-1),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "KNeighborsRegressor":KNeighborsRegressor(n_jobs=-1)
            }
            # params
            params = {
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'splitter':['best','random'],
                    'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'criterion':['squared_error', 'friedman_mse'],
                    'max_features':['sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{

                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "KNeighborsRegressor":{
                    "weights":["uniform", "distance"],
                    "algorithm":["auto", "ball_tree", "kd_tree"]
                }                
            }
            score, model = get_best_model(
                models=models, 
                X_train=X_train, 
                X_test=X_test, 
                y_train=y_train, 
                y_test=y_test, 
                params=params
            )

            save_object(
                obj=model, file_path=self.model_path
            )
            logging.info(f"model '{model}' saved successfully.")
            return score

        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
