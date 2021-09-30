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
    if request.method == 'POST':
        query = request.json["image"]
        client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['Snappp']
        collection = db["AddOneToCanvas"]
        collection.insert_one(query)
        return jsonify({"status":"Success"})
        
    
    return jsonify({"status":"200"})
if __name__ == '__main__':
    app.run()