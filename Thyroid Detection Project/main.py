from wsgiref import simple_server
from flask import Flask,request,Response
from flask_cors import cross_origin,CORS
import flask_monitoringdashboard as dashboard
import os

os.putenv('LANG', 'en_US.UTF-8') # for the deployment purpose
os.putenv('LC_ALL', 'en_US.UTF-8') # for the deployment purpose

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/train",methods=["POST"])
@cross_origin()
def trainRouteClient() :
    try :
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']


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