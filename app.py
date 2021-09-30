from flask import Flask, jsonify, request
app = Flask(__name__)
import requests
import json
import urllib.request,urllib.parse,urllib.error
from flask_cors import CORS, cross_origin

CORS(app, support_credentials=True)



@app.route("/api/", methods = ["POST","GET"])
@cross_origin(origin='*')
def tenorimages():
    result = {}
    if request.method == 'POST':
        result["a"]={"a":"a"}
    
    return jsonify(result)

if __name__ == '__main__':
    app.run()