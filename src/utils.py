import os, sys
import numpy as np
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException

def save_object(file_path, obj): # bunu data_transformation dosyasinda kullaniyor
    try:
        dir_path = os.path.dirname(file_path) # bu ile dosyanin yolu elde edilir

        os.makedirs(dir_path, exist_ok=True) # eger bir dizin yoksa olusturur. 

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

# bu kod pipeline veya egitilmis modelleri diske yazar
# gerektiginde tekrardan kolayca cagirabilmek icin