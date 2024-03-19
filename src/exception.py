import sys
from src.logger import logging

def error_message_detail(error, error_detail):
    _,_,exc_tb = error_detail.exc_info()  # alt cizgi ilgilenmedigimiz degeri atlamak icin kullanilir
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message".format(
    file_name, exc_tb.tb_lineno, str(error))

    return error_message

    


class CustomException(Exception): # hatalar Exception sinifi kullanilir ve ilave olarak kendimizde hata mesajlari ekleyebiliriz
        def __init__(self, error_message, error_detail:sys):
            super().__init__(error_message)
            self.error_message = error_message_detail(error_message, error_detail=error_detail)

        def __str__(self):
            return self.error_message    


# Custom exception ile Exception paketine dahil olarak daha 
# daha detayli hata mesajlari ekleyebiliriz
# böylece hata daha iyi tanimlanmis olur


if __name__ == '__main__':
    try : 
        a = 1/0
    except Exception as e:
        logging.info('Divide by zero')
        raise CustomException(e, sys)

    
    