# _*_ coding: utf-8 _*_

import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Input, Embedding
from keras.utils import np_utils
from keras.callbacks import EarlyStopping
import csv
import random
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
from numpy import array, argmax
import flask
from flask import Flask, request, session, render_template
import io
import tensorflow as tf
from keras.backend import clear_session


# 랜덤시드 고정시키기
np.random.seed(5)
# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None
dataset = None

def load_model():
	global model
	model = ResNet50(weights="imagenet")
    
def makeWindowMat(seqData):
    dataset_x = []
    for i in range(len(seqData) - 3):
        subset = seqData[i : ( i + 4 + 1)]
        for si in range(len(subset)):
            dataset_x.append(subset[si][:15])
    return np.array(dataset_x)

@app.route("/predict", methods=["POST"])
def predict():
    from keras.models import load_model
    model = load_model('wifi_LSTM_model4.h5')
    
    f = open('./sample_data.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)

    WiFiData = []
    for line in rdr:
        tmp = []
        for i in range(15):
            tmp.append((line[i]))
        WiFiData.append(tmp)
    f.close()
    x_train = makeWindowMat(WiFiData)
    x_train = np.reshape(x_train, (1, 4, 15))
    model = load_model('wifi_LSTM_model4.h5')
    pred_out = model.predict(x_train, batch_size=1)
    
    clear_session() #TODO::중요!!
    
    idx = np.argmax(pred_out[0]) # one-hot 인코딩을 인덱스 값으로 변환
    print(idx)
#     return ("good")
    return flask.jsonify({'you sent noting': 'good'})
# 	# return the data dictionary as a JSON response
# 	return flask.jsonify(data)


@app.route('/predict2', methods=["POST"])
def predict2():
    json = request.get_json()
    mydata = array(json['Level1'])
    print(mydata)
    tmpdata = np.zeros((2,15))
    tmpdata[0] = mydata
    tmpdata[1] = mydata
    
    from keras.models import load_model
    model2 = load_model('wifi_multi_perceptron_model6.h5')
    yhat = model2.predict_classes(tmpdata[0:1])
    print(yhat[0])
    clear_session()
    
    return str(yhat[0])

@app.route('/predict3', methods=["POST"])
def predict3():
    json = request.get_json()
    mydata = array(json['Level1'])
    mydata2 = array(json['Level2'])
    mydata3 = array(json['Level3'])
    mydata4 = array(json['Level4'])
    mydata5 = array(json['Level5'])
    print(json['Level1'])
    print(mydata)
    print(mydata2)
    print(mydata3)
    print(mydata4)
    print(mydata5)
#     tmpdata = np.zeros((2,50))
#     tmpdata[0] = mydata
#     tmpdata[1] = mydata
#     from keras.models import load_model
#     model2 = load_model('wifi_reg_perceptron_model1.h5')
#     yhat = model2.predict_classes(tmpdata[0:1])
#     clear_session()
#     return str(yhat[0])# + " PERCEP"
    if json['isLSTM'] == 'F':
        tmpdata = np.zeros((2,15))
        tmpdata[0] = mydata
        tmpdata[1] = mydata
        from keras.models import load_model
        model2 = load_model('wifi_reg_perceptron_model6.h5')
        yhat = model2.predict_classes(tmpdata[0:1])
        clear_session()
        return str(yhat[0])# + " PERCEP"
    else :
        tmpdata = np.zeros((1,4,15))
        tmpdata[0][0] = mydata2
        tmpdata[0][1] = mydata3
        tmpdata[0][2] = mydata4
        tmpdata[0][3] = mydata5
        from keras.models import load_model
#         model = load_model('wifi_LSTM_model6.h5')
        model = load_model('wifi_result_LSTM_normal_path2.h5')
        pred_out = model.predict(tmpdata, batch_size=1)
        clear_session() #TODO::중요!
        idx = np.argmax(pred_out[0]) # one-hot 인코딩을 인덱스 값으로 변환
        return str(idx)# + " LSTM"
    
    print(mydata)
    tmpdata = np.zeros((2,15))
    tmpdata[0] = mydata
    tmpdata[1] = mydata
    
    from keras.models import load_model
    model2 = load_model('wifi_multi_perceptron_model4.h5')
    yhat = model2.predict_classes(tmpdata[0:1])
    print(yhat[0])
    clear_session()
    
    return str(yhat[0])

@app.route('/')
def hello_world():
    return 'hello_world'

def myFunc():
    from keras.models import load_model
    global model
    model = load_model('wifi_multi_perceptron_model4.h5')
    global dataset
    dataset = np.loadtxt("./made_wifi4.csv", delimiter=",")#TODO:: 파일 변경 시 수정

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	app.debug = True
# 	myFunc()
	app.run(host = '164.125.34.170', port = 8080)