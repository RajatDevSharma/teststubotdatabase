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
            "displayText": output,
            #"data": {"http://www.thapar.edu/images/phocagallery/nava_nalanda_central_library/thumbs/phoca_thumb_l_unnamed.jpg"},
            # "contextOut": [],
            "source": "python_stubot"
        }
    
    if req.get("result").get("action") == "available.book.title":
        
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
            "displayText": output,
            #"data": {"http://www.thapar.edu/images/phocagallery/nava_nalanda_central_library/thumbs/phoca_thumb_l_unnamed.jpg"},
            # "contextOut": [],
            "source": "python_stubot"
        }
    
    if req.get("result").get("action") == "new.book.library":
        
        coll = db.librarysample
        bookResult = coll.find({'stat':"new"})
        length =bookResult.count()
        
        output=""
        if length == 0:
            output = "No new books available"
            
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
            "displayText": output,
            #"data": {""},
            # "contextOut": [],
            "source": "python_stubot"
        }
    if req.get("result").get("action") == "best.soc":
        
        coll = db.Societies
        search="good"
        rgx = re.compile('.*' +search+ '.*', re.IGNORECASE)
        bookResult = coll.find({"$or":[{'SocToDo':rgx}, {'SocTags':rgx}]})
        length =bookResult.count()
        
        output=""
        if length == 0:
            output = "all are good"
            
        for i in bookResult:
            bookEntity = i['SocName']
            if length != 1:
                output = output + bookEntity + ' || '
            elif length ==1:
                output = output + bookEntity
            length = length -1
        
        return {
            "speech": output,
            "displayText": output,
            #"data": {""},
            # "contextOut": [],
            "source": "python_stubot"
        }
    
    if req.get("result").get("action") == "soc.interest":
        
        result = req.get("result")
        parameters = result.get("parameters")
        book = parameters.get("interests")
        coll = db.Societies
        search = book
        rgx = re.compile('.*' +search+ '.*', re.IGNORECASE)
        bookResult = coll.find({"$or":[{'SocToDo':rgx}, {'SocTags':rgx}]})
        length =bookResult.count()
        
        output = ""
        if length == 0:
            output = "Society Not Available"
            
        for i in bookResult:
            bookEntity = i['SocName']
            if length != 1:
                output = output + bookEntity + ' || '
            elif length ==1:
                output = output + bookEntity
            length = length -1
        
        return {
            "speech": output,
            "displayText": output,
            #"data": {"http://www.thapar.edu/images/phocagallery/nava_nalanda_central_library/thumbs/phoca_thumb_l_unnamed.jpg"},
            # "contextOut": [],
            "source": "python_stubot"
        }
    
    if req.get("result").get("action") == "soc.info":
        
        result = req.get("result")
        parameters = result.get("parameters")
        book = parameters.get("Societies")
        coll = db.Societies
        search = book
        rgx = re.compile('.*' +search+ '.*', re.IGNORECASE)
        bookResult = coll.find({'SocName':rgx})
        length =bookResult.count()
        
        output = ""
        if length == 0:
            output = "Sorry, could not find"
        
        logo =  ""
        for i in bookResult:
            bookEntity = i['SocToDo']+'Contact : '+i['SocContact']
            logo = logo + i['SocImg']
            if length != 1:
                output = output + bookEntity + ' || '
            elif length ==1:
                output = output + bookEntity
            length = length -1
        
        return {
            "speech": output,
            "displayText": output,
            "data" : {
                "facebook" : {
                    "attachment" : {
                        "type" : "template",
                        "payload" : {
                            "template_type" : "generic",
                            "elements" : [ 
                                {
                                    "title" : book,
                                    "image_url" : logo
                                }
                            ]
                        }
                    }         
                }
            },
            '''
            "messages": [
                {
                    "type": 0,
                    "speech": output,
                    "platform": "facebook"
                }
            ],
            '''
            #"data": {""},
            # "contextOut": [],
            "source": "python_stubot"
        }
        

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
