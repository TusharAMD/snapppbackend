from flask import Flask, jsonify, request
app = Flask(__name__)
import requests
import json
import urllib.request,urllib.parse,urllib.error
from flask_cors import CORS, cross_origin
import pymongo
import base64

# To avoid any CORS Issue
CORS(app, support_credentials=True)


# This is api endpoint to get tenor images from tenor api and on POST request send images to frontend
@app.route("/api/", methods = ["POST","GET"])
@cross_origin(origin='*')
def tenorimages():
    result = {}
    imgbb = []
    result["tenor"] = [] 
    if request.method == 'POST':
        apikey = "FMSOZTYHFB4D"  # key value
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
                imgbb.append(url)
        
        for i in range (0,len(imgbb)):
            img_data = requests.get(imgbb[i]).content
            with open('Output.gif', 'wb') as handler:
                handler.write(img_data)
                
            with open("Output.gif", "rb") as file:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": "c4b63af118f97f88cdeea980cdb4d6c9",
                    "image": base64.b64encode(file.read()),
                }
                res = requests.post(url, payload)
                img = res.json()["data"]["url"]
                result["tenor"].append(img)
        
        else:
            top_8gifs = None
    
    return jsonify(result)

# This is used to get image from tool box and send to Canvas
@app.route("/addonetocanvas/", methods = ["POST","GET"])
@cross_origin(origin='*')
def addonetocanvas():

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/Snappp?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client['Snappp']
    collection = db["AddOneToCanvas"]
    if request.method == 'POST':
        if request.json["flag"]==1:
            query = request.json
            print(query)
            email=request.json["user"]
            x = collection.find_one({"email":email})
            if x:
                prevUrl = x["image"]
                myquery = { "image": prevUrl }
                newvalues = { "$set": { "image": query["image"] } }
                collection.update_one(myquery,newvalues)
            else:
                collection.insert_one({"email":email,"image":query["image"]})
            
            return jsonify({"status":"Success"})        
        else:
            email=request.json["user"]
            x = collection.find_one({"email":email})
            img = x["image"]
            return jsonify({"image":img})
    
    return jsonify({"status":"200"})

# When post request is performed on this endpoint we would get snap image from that specific user (user detail is send from frontend)
@app.route("/getpwa/", methods = ["POST","GET"])
@cross_origin(origin='*')
def getpwa():

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/Snappp?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client['Snappp']
    collection = db["pwa"]
    
        
    if request.method == 'POST':
        email=request.json["user"]
        x = collection.find_one({"email":email})
        img = x["image"]
        print(img)
        return jsonify({"image":img})

    return jsonify({"status":"200"})
  
# When Save button is pressed a axios request is made and SVG data is send to backend. Now here we save the data to the mongodb database according to email id we got from frontend    
@app.route("/html2canvas/", methods = ["POST","GET"])
@cross_origin(origin='*')
def html2canvas():

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/Snappp?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client['Snappp']
    collection = db["memecreated"]
    
        
    if request.method == 'POST':
       print(request.json["data"])
       fh=open("abc.txt","w")
       fh.write(request.json["data"])
       data=request.json["data"]
       user=request.json["user"]
       
       collection.insert_one({"user":user,"data":data,"upvotedby":[user]})
    return jsonify({"status":"200"})
    

# This endpoint serves the purpose to give information of memes collection made by the particular user
@app.route("/profile/", methods = ["POST","GET"])
@cross_origin(origin='*')
def profile():

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/Snappp?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client['Snappp']
    collection = db["memecreated"]
    
        
    if request.method == 'POST':
       if "user" in request.json and len(request.json.keys())==1:
           user=request.json["user"]
           posts=collection.find({"user":user})
           #print(user,posts)
           result=[]
           for ele in posts:
            result.append(ele["data"])
           return jsonify({"result":result})
       elif "upvotedby" in request.json:
           user=request.json["user"]
           posts=collection.find({"user":user})
           #print(user,posts)
           result=[]
           for ele in posts:
            result.append(ele["upvotedby"])
           return jsonify({"upvotedby":result})
    return jsonify({"status":"200"})

# When upvote is done the user who has upvoted must be send to database and to avoid mutiple upvotes we are using sets in python
@app.route("/voting/", methods = ["POST","GET"])
@cross_origin(origin='*')
def voting():

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/Snappp?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client['Snappp']
    collection = db["memecreated"]
        
    if request.method == 'POST':
       user=request.json["user"]
       img=request.json["img"]
       upvoter=request.json["upvoter"]
       posts=collection.find_one({"user":user,"data":img})
      
       temp=posts["upvotedby"]
       temp.append(upvoter)
       temp=list(set(temp))
       print(temp)
       myquery = {"user":user,"data":img}
       newvalues = {"$set": {"upvotedby": temp}}
       collection.update_one(myquery, newvalues)
       
       
    return jsonify({"status":"200"})

if __name__ == '__main__':
    app.run(debug = True, ssl_context='adhoc')
