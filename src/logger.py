import logging 
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok= True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", # bunlar logger da gözükecek bilgiler satir numarasida gözükecek
    level= logging.INFO
)

# burda kod ile bir dosya aciyor ve her dosyada orda gerceklesen
# loglar kaydediliyor. Bir youtube videosunda tüm loglar
# bir dosyada gözüküyordu ama bu daha iyi büyük programlarda o anda
# gerceklesen tüm loglar ayni klasörde gözükebilir