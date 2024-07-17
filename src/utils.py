import os
import sys
import dill 

import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging

from sklearn.metrics import r2_score

def save_object(file_path, obj):
    try:
        logging.info(f"Saving object to {file_path}")
        dir_path=os.path.dirname(file_path)
        logging.info(f"Creating directory {dir_path} if not exists")
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            logging.info(f"Opening file {file_path} for writing")
            dill.dump(obj, file_obj)
            logging.info(f"Object saved successfully to {file_path}")

    except Exception as e:
        logging.error(f"Error saving object: {e}")
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models):
    try:
           report = {}

           # Iterate over the models dictionary
           for i in range(len(list(models))):
               model = list(models.values())[i]

               model.fit(X_train, y_train)

               y_train_pred = model.predict(X_train)
               y_test_pred = model.predict(X_test)
               train_model_score = r2_score(y_train, y_train_pred)
               test_model_score = r2_score(y_test, y_test_pred)

               report[list(models.keys())[i]] = test_model_score

           return report
        
    except Exception as e:
         raise CustomException(e,sys)