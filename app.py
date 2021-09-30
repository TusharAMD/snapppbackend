from flask import Flask, jsonify, request
app = Flask(__name__)
import requests
import json
import urllib.request,urllib.parse,urllib.error
from flask_cors import CORS, cross_origin
import pymongo

CORS(app, support_credentials=True)



@app.route("/api/", methods = ["POST","GET"])
@cross_origin(origin='*')
def tenorimages():
    result = {}
    result["tenor"] = [] 
    if request.method == 'POST':
        apikey = "FMSOZTYHFB4D"  # test value
        lmt = request.json["lmt"]
        r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % apikey)

        if r.status_code == 200:
            anon_id = json.loads(r.content)["anon_id"]
        else:
            anon_id = ""
        search_term = request.json["search_term"]
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" %   
             (search_term, apikey, lmt, anon_id))

        if r.status_code == 200:
            top_8gifs = json.loads(r.content)
            for i in range(len(top_8gifs['results'])):
                url = top_8gifs['results'][i]['media'][0]['gif']['url']
                result["tenor"].append(url)
        else:
            top_8gifs = None
    
    return jsonify(result)


@app.route("/addonetocanvas/", methods = ["POST","GET"])
@cross_origin(origin='*')
def addonetocanvas():

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/Snappp?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client['Snappp']
    collection = db["AddOneToCanvas"]
    if request.method == 'POST':
        query = request.json
        x = collection.find_one()
        prevUrl = x["image"]
        myquery = { "image": prevUrl }
        newvalues = { "$set": { "image": query["image"] } }
        
        collection.update_one(myquery,newvalues)
        return jsonify({"status":"Success"})
        
    if request.method == 'GET':
        x = collection.find_one()
        img = x["image"]
        return jsonify({"image":img})
    
    return jsonify({"status":"200"})
if __name__ == '__main__':
    app.run(debug = True)