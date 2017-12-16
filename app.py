import os
import urllib
import json
import re
import pymongo 

from flask import Flask
from flask import request
from flask import make_response

from pymongo import MongoClient

app = Flask(__name__)

#client = MongoClient( "mongodb://rajatdev:rdsharma@ds059207.mlab.com:59207/heroku_lgz52rzd")

#db = client.heroku_lgz52rzd

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "search.book.title":
        
        #collection = db.librarysample
        
        result = req.get("result")
        parameters = result.get("parameters")
        book = parameters.get("title")
        
        '''
        #find_book="discrete"
        speech=""
        for i in book:
            find_book=i
        
        matches = [x for x in books if re.search(find_book, x, re.M|re.I)]
        
        if len(matches)==0:
            speech="Not available"
        
        for i in matches:
            speech= speech + i + " , " 
            
        print("Response:")
        print(speech)
        '''
        '''
        a=[]
        bookResult = collection.find( {"title":book} )
        for i in bookResult:
            a.append(i["title"])
        '''
        return {
            "speech": "hello",
            "displayText": "hello",
            #"data": {},
            # "contextOut": [],
            "source": "python_stubot"
        }
'''
@app.route("/")
def start():
    a=[]
    result = collection.find()
    for i in result:
        a.append(i["title"])
    return a[0]
'''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
