# these are some flask libraries imported!
from wsgiref import simple_server
from flask import Flask, request, render_template, Response
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard

import os
import json

from training_validation_insertion import train_validation
from trainingModel import trainModel

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    print('home')
    return render_template('index.html')

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try :
        if(request.json['folderPath'] is not None):
            print('path is not None')

            path = request.json['folderPath'] # setting the path variable that we are receiving through the POST request
            print('path variable set')
            #train_valObj = train_validation(path) # initializing the object
            #print('train_validation obj init done now calling the method ...')
            #train_valObj.train_validation() # calling the method
            #print('back to home ')

            trainModelObj = trainModel() # object initialization
            print('train model object init done now calling the method')
            trainModelObj.trainingModel() # calling the method
            print('back to main.py ')


    except ValueError :
        return Response('Error Occurred!!!  %s' % ValueError)

    except KeyError :
        return Response('Error Occurred!!!  %s' % KeyError)

    except Exception as e :
        return Response('Error Occurred!!!  %s' % e)

    return Response( " Training Successfully Completed :) !!!")



if __name__ == '__main__' :
    host = '0.0.0.0'
    port = 1997
    httpd = simple_server.make_server(host,port,app)
    print('Starting the application....')
    print('Serving on port localhost:%d'%(port))
    httpd.serve_forever()
