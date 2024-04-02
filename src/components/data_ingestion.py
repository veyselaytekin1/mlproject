import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig


@dataclass  # bunun ile __init__ yapmadan direk degiskenlerini tanimlayabiliyorsun # ama icine bir fonksiyon yazacaksan __init__ kullan dedi
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', 'train.csv')
    test_data_path: str=os.path.join('artifacts', 'test.csv')
    raw_data_path: str=os.path.join('artifacts', 'data.csv')

# bu galiba train ve test datalarini nerede tuttugunu bilen bir component
# bu yazdigimiz path'ler ile
# asagida artifact adinda bir dosya olusacak, bunlar kullanilarak
# ve data klasöründen data okunacak, data train_test siplit ile 
# artifacts dosyasina kaydedilecek




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
        # bu yukarda yazdigimiz yolu bu classta kullanmak icin hazirlanmis
        # bunun ile(self) DataIngestion classina aliniyor. ve bir asagidakinde kullanilacak
    

    def initiate_data_ingestion(self): # data okumak icin 
        logging.info('Entered the data ingestion method or component')
        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as DataFrame')

            # burda csv den data okumayi tercih etti ilerde MongoDB den data alacam dedi
            # istersen kodlarini API dan veya database den cekecek sekilde ayarlayabilirsin dedi

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            # bunun ile artifacts adinda bir klasör olusuyor, ve icine train_data_path kullanilarak
            # bir train file olusturuluyor

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            # bunun ile data asagida bölünmeden önce tüm hali kaydediliyor

            logging.info('Train test split initiated')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            # burda datalar bölünüyor ve asagiya paket halinde veriliyor

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            #burda alinan veriler csv ye kaydediliyor, en yukarida belirtilen pathler bir daha kullaniliyor

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


# benim anladigim: model_trainer dosyasini yazdiktan sonra modeli bu dosyayi calistirarak 
# train etti, ve cikti aldi. ve bunu simdilik ana dosyagibi yapti, projeyi burdan calistiriyor
# aslinda tüm istedigi dosyalarda bunu yapabilirdi. burdaki gerekli adimlari ve fonksiyonlari 
# impport edererk


#Proji yürütmek icin Ingestion dosysini secmis galiba 
# burda asagida  önce datayi alacak, sonra transformation islemleri uygulayacak
# ve bir adim sonra train islemleri uygulayacak

if __name__=='__main__':
    obj=DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    # bu son satir return olan degerleri buna atiyor, 
    # iki tane return degeri dönüyor üstte
    # ve sadece path yapmiyor, datayi train test diye bölüyor ve bu yeni olusturulan datalarin
    # gercek yolu
    # en yukardaki sadece sözde bir yoldu, o öyle kalmasi bir anlam ifade etmezdi
    # cünkü daha train_test ile bölünmemisti, initiate_data_ingestion() bunun return ile
    # dosyalarin yolu tam netllesmis oluyor
    

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)
    # galiba data_transformation dosyasindaki bütün kod bulogu bu satira gizlenmis
    # onun icin python src/components/data_ingestion.py bu komut ile dosyayi calistidi
    # cünkü zaten bu calisirsa data_transformation dosyasi calismis olacak
    # bu kod ile veri setine uygulanacak transformation islemleri yani 
    # data_transformation dosyasindaki preprocessing_obj bu ifadede gizlenmis olan
    # columnTransformer ifadesi ndeki Standartscaler ve OneHotencoder uygulandiktan sonra
    # verinin array halini retuen ediyordu, burda o return edilen degerler 
    # degiskene ataniyor


    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))


    




