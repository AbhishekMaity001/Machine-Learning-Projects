from flask import Flask,render_template,request,redirect
import os


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

app.run(debug=True)