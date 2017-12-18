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

client = MongoClient( "mongodb://rajatdev:rdsharma@ds059207.mlab.com:59207/heroku_lgz52rzd")

db = client.heroku_lgz52rzd

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
        
        collection = db.librarysample
        
        result = req.get("result")
        parameters = result.get("parameters")
        book = parameters.get("title")
        title = ""
        for i in book:
            title = i
        #a=[]
        #bookResult = collection.find( {"availabilty":"yes"} )
        rgx = re.compile('.*' + title + '.*' , re.IGNORECASE)
        bookResult = collection.find( {"title": rgx} )
        length = bookResult.count()
        
        output = ""
        if length == 0:
            output = "Book Not Available"
            
        for i in bookResult:
            #a.append(i["author"])
            bookEntity = i["title"] + " by " + i["author"]
            if length != 1:
                output = output + bookEntity + ' || '
            elif length ==1:
                output = output + bookEntity
            length = length -1
        
        return {
            "speech": output,
            '''
            "messages": [
                {
                    "type": 0,
                    "speech": "look at that image"
                },
                {
                    "type": 3,
                    "imageUrl": "http://www.thapar.edu/images/phocagallery/nava_nalanda_central_library/thumbs/phoca_thumb_l_unnamed.jpg"
                }
            ],
            '''
            "displayText": output,
            #"data": {"http://www.thapar.edu/images/phocagallery/nava_nalanda_central_library/thumbs/phoca_thumb_l_unnamed.jpg"},
            # "contextOut": [],
            "source": "python_stubot"
        }
    if req.get("result").get("action") == "new.book.library":
        
        collection = db.librarysample
        
        

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
