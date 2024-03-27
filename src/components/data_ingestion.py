import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass



@dataclass  # bunun ile __init__ yapmadan direk degiskenlerini tanimlayabiliyorsun
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', 'train.csv')
    test_data_path: str=os.path.join('artifacts', 'test.csv')
    raw_data_path: str=os.path.join('artifacts', 'data.csv')

# bu galiba train ve test datalarini nerede tuttugunu bilen bir component
# bu yazdigimiz path'ler ile
# ama icine bir fonksiyon yazacaksan __init__ kullan dedi

# "2yol" eger @dataclass yapisini kullanmak istemez isen
# class DataIngestionConfig:
#     def __init__(self, train_data_path: str = os.path.join('artifacts', 'train.csv'),
#                 test_data_path: str = os.path.join('artifacts', 'test.csv'),
#                 raw_data_path: str = os.path.join('artifacts', 'data.csv')):
#         self.train_data_path = train_data_path
#         self.test_data_path = test_data_path
#         self.raw_data_path = raw_data_path


# yukarida yapilan class yapisi asagida kullanilacak, ve datalarin yollarini gösterir
# bu sekilde güzel bir yapida olur. kod okunmasi icin


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() # bu yukardakini tetikleyecek

    def initiate_data_ingestion(self): # data okumak icin 
        logging.info('Entered the data ingestion method or component')
        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as DataFrame')

            # burda csv den data okumayi tercih etti ilerde MongoDB den data alacam dedi
            # istersen kodlarini API dan veya database den cekecek sekilde ayarlayabilirsin dedi

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info('Train test split initiated')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Ingestion of data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                # aralarindaki nokta isareti ingestion_config yukarida 
                # DataIngestionConfig buna atanmisti ve artik bunun icinden 
                # bilgi yani train_data_path bunun ile baglanti kurmak icin konuldu
                # bu bence ilerde tranformation bölümünde kullanilacak
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__=='__main__':
    obj=DataIngestion()
    obj.initiate_data_ingestion()


