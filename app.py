from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.exception import CustomException
from src.logger import logging

application = Flask(__name__)

app = application

## Route for home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score')))


        pred_df = data.get_data_as_data_frame()
        logging.info('Data is getting as DataFrame')
        print(pred_df)

        predict_pipeline = PredictPipeline() # bunun icinde bir asagida olan predict function var o bize predict yapacak
        results = predict_pipeline.predict(pred_df)
        return render_template('home.html', results = results[0])
        # home.html dosysinin en sonunda results degiskenini görüyoruz.
        # yani burda yapilanlar, orda gözükecek
        
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001)        
       
