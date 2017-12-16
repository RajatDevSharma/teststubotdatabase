import os
from flask import Flask
import pymongo 
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient( "mongodb://rajatdev:rdsharma@ds059207.mlab.com:59207/heroku_lgz52rzd")

db = client.heroku_lgz52rzd
collection = db.librarysample

@app.route("/")
def start():
    a=[]
    result = collection.find()
    for i in result:
        a.append(i["title"])
    return a[0]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
