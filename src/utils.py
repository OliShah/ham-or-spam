import os
import sys
import dill 

import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging

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