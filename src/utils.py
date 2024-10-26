import sys
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from src.exception import CustomException
import pickle
from src.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score



# data_ingestion
def get_splits(data:pd.DataFrame) -> tuple:
    """
    #### Description: {
    test_size=0.33, random_state=42
    
    #### }
    #### params:
    - data: dataframe or array like
    #### returns: It returns tuple of train and test data.
    """
    try:
        train_df, test_df = train_test_split(data, test_size=0.33, random_state=42)
        return (train_df, test_df)
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)
    

# data_transformation
def get_transformer(num_features:list[str], cat_features:list[str]):
    """
    #### params:
    - train_df: train data dataframe or array like
    - test_df: test data dataframe or array like
    #### returns: transformer object
    """
    try:
        num_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")), 
                ("scaler", StandardScaler())
            ]
        )

        cat_pipeline = Pipeline(
            steps=[
                ("encoder", OneHotEncoder(drop="first")),
                ("imputer", SimpleImputer(strategy="most_frequent")), 
                ("scaler", StandardScaler(with_mean=False))
            ]
        )

        preprocessor = ColumnTransformer(
            [
                ("num_pipeline", num_pipeline, num_features),
                ("cat_pipeline", cat_pipeline, cat_features)
            ]
        )

        return preprocessor

    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)


# save object
def save_object(obj, file_path:str):
    """
    This function saves the object into a pickle file on given path.
    """
    try:
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            return None
    except Exception as e:
        raise CustomException(e, sys)


# model_trainer
def get_best_model(models:dict, X_train, X_test, y_train, y_test, params:dict):
    """
    returns: best score and best model as a tuple.
    """
    try:
        score_and_model = dict()
        best_score = 0.00
        for model_name in models.keys():
            model_obj = models[model_name]
            param =  params[model_name]
            
            gs = GridSearchCV(estimator=model_obj, param_grid=param, 
                                cv=3, n_jobs=-1)
            gs.fit(X_train, y_train)
            model_obj.set_params(**gs.best_params_)
            model_obj.fit(X_train, y_train)
            pred = model_obj.predict(X_test)
            score = r2_score(y_test, pred)
            score_and_model[score] = model_obj

        for model_score in score_and_model.keys():
            if model_score > best_score:
                best_score = model_score

        best_model = score_and_model[best_score]
        return (best_score, best_model)

    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)


# prediction_pipeline
def get_dataframe(gender:str,
                  race_ethnicity:str,
                  parental_level_of_education:str, 
                  lunch:str, 
                  test_preparation_course:str, 
                  reading_score:float,
                  writing_score:float
                  ):
    try:
        data = {
            "gender":[gender],
            "race_ethnicity":[race_ethnicity],
            "parental_level_of_education":[parental_level_of_education], 
            "lunch":[lunch], 
            "test_preparation_course":[test_preparation_course], 
            "reading_score":[reading_score],
            "writing_score":[writing_score]
        }
        dataframe = pd.DataFrame(data)
        return dataframe
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)


# load object
def load_object(path):
    try:
        with open(path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)

