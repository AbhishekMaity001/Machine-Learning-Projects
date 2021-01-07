from wsgiref import simple_server
from flask import Flask,request,Response
from flask_cors import cross_origin,CORS
import flask_monitoringdashboard as dashboard
import os

from training_validation_insertion import train_validation
from trainingModel import trainModel

from prediction_validation_insertion import pred_validation
from Predict_From_Model import prediction

os.putenv('LANG', 'en_US.UTF-8') # for the deployment purpose
os.putenv('LC_ALL', 'en_US.UTF-8') # for the deployment purpose

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/predict",methods=["POST"])
@cross_origin()
def predictRouteClient():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            #pred_val = pred_validation(path)
            #pred_val.prediction_validation()

            pred = prediction(path)
            path = pred.prediction_From_Model()

            return Response("Prediction file created successfully %s !!!"%path)

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train",methods=["POST"])
@cross_origin()
def trainRouteClient() :
    try :
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            #train_val = train_validation(path) # Object init
            #train_val.train_validation() # Calling the function

            train_model = trainModel() # Object init
            train_model.trainingModel() # Calling the function




    except KeyError :
        return Response("Key Error Occurred !! :: %s"%KeyError)
    except ValueError :
        return  Response("Value Error Occurred !! :: %s"%ValueError)
    except Exception as e:
        return Response("Error Occurred !! :: %s"%e)
    return Response("Successfull end of Training!!! ")

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 1997
    httpd = simple_server.make_server(host,port,app)
    print("Starting the Application....!!")
    print("serving on port localhost:%s"%port)
    httpd.serve_forever()