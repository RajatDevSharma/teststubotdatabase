import os
#from flask import Flask
from flask import Flask, render_template, request, redirect 
import pymongo 
from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGODB_URI') 
client = MongoClient(MONGO_URL)

db = client.stubot1 
collection = db.librarysample

app = Flask(__name__)

'''
@app.route("/", methods=['GET']) 
def index(): 
    shouts = collection.find() 
    return render_template('index.html', shouts=shouts)

@app.route("/post", methods=['POST']) 
def post():
    shout = {"name":request.form['name'], "message":request.form['message']} 
    shout_id = collection.insert(shout)
    return redirect('/')

'''

@app.route("/")
def hello():
    result = collection.find( { availabilty: "no" } )
    return "hello"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
