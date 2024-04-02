# feature engineering ve data cleaning
# feature tiplerii degistirebiliriz
# tüm EDA islemlerini burda yapabiliriz
# missing value , filling gibi islemler


import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    # buraya model kaydedilmiyor, dataya yapilan preprocessing islemleri kaydediliyor
    # yeni gelen datalara direkt uygulaniyor

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        """This function is reponsible for data transformation"""
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            num_pipeline = Pipeline(

                steps= [
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps= [
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False)) # galiba categoric oldugu icin, mean alinmaz
                    # burda normalde categoric bir veriye StandardScaler uygulanmaz ama hemen bir satir üsste 
                    # OneHot onlari 0,1 yaptigi icin uygulanabilir ama uygulandiginda genelde sifirlar olur
                ]
            )
            logging.info('Numerical  column encoding completed')
            logging.info('Categorical column encoding completed')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipelines', cat_pipeline, categorical_columns)
                ]
            )
            # bu pipeline ile yukardaki islemler ColumnTransformer hazir pipe ile birlestiriliyor

            return preprocessor
            # ve hazir halde kullanilacak pipeine ifade eder, yani pipeline edilmis veri degil,
            # sadece yapilacakislemi saklar icinde

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):
        # bu data_ingestion dosyasinda kullanilacak

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformer_object()
            # bunun icinde yukarida tanimlanan ColumnTransformer () standart sclaer ve
            # OneHot encoder islemleri sakli

            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']

            input_feature_train_df = train_df.drop(columns = [target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns = [target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on trainin dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            # bu fit_transform kendi basina birsey yapmaz, önceden belirlenen veriye uygulanacak
            # islemleri veriye uygular mesela preprocessing_obj bu yukarida Columntransformer 
            # ifadesi icinde gizlenen degerler ve fit_transform ile train setine uygulaniyor

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            #bu transform islemi uygulanan veri setine numpy array olarak veriyor

            logging.info(f"Saved preprocessing object")

            save_object( #utils dosyasinda tanimlanmis

                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)

# bunun sonuna if __name__=='__main__': gibi bisey yapmadi 
# cünkü bunu calistirmak istemiyor, burdakileri data_ingestion.py de kullaniyor import ile
