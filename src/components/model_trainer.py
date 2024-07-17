# https://www.youtube.com/watch?v=EAWR1kFtEGo

import os 
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    GradientBoostingClassifier, 
    RandomForestClassifier, 
    AdaBoostClassifier,
    )

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object 
from src.utils import evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artefacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")

            # Split the train and test arrays into features and labels
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],  # Features of the training data (all columns except the last)
                train_array[:, -1],   # Labels of the training data (last column)
                test_array[:, :-1],   # Features of the test data (all columns except the last)
                test_array[:, -1]     # Labels of the test data (last column)
            )

            # dictionary of models
            models={
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Linear Regression": LinearRegression(),
                "K-neighbours Classifier": KNeighborsRegressor(),
                "XGBClassifier": XGBRegressor(),
                "CatBoosting Classifier": CatBoostRegressor(verbose=False),
                "AdaBoost Classifier": AdaBoostClassifier()
            }
            
            # evaluate models and return their performance report as a dict
            model_report:dict=evaluate_models(
                X_train=X_train, y_train=y_train, 
                X_test=X_test, y_test=y_test, 
                models=models                
            )
            
            # best model score
            best_model_score = max(sorted(model_report.values()))

            # best model name
            best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("Best model not found")
            
            logging.info(f"Best found model on both training and testing dataset")

            # save the best model to specified path
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            # use best model to make preds on test data
            predicted=best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square  

        except Exception as e:
            raise CustomException(e,sys)