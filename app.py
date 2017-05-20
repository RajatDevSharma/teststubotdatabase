#!/usr/bin/env python

import urllib
import json
import os
import re

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


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
    if req.get("result").get("action") != "search.book.title":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    book = parameters.get("title")
    #find_book="discrete"
    speech=""
    for i in book:
        find_book=i
    books=['Discrete Mathematics', 'Algorithms I', 'Programming and Data Structures', 'Software Engineering', 'Switching Circuits and Logic Design', 'Formal Languages and Automata Theory', 'Operating Systems', 'Compilers', 'Foundations of Computing', 'Computer Organization and Architecture', 'Theory of Computation', 'Algorithms 2013 II', 'Computer-Networks', 'Symbolic Logic and Automated Reasoning', 'Principles of Programming Languages', 'Symbolic Logic and Automated Reasoning', 'Artificial Intelligence', 'Electronic Design Automation', 'Image Processing', 'Applied Graph Theory', 'Computational Geometry', 'Computational Complexity', 'Advanced Computer Architecture', 'VLSI System Design', 'Multimedia Applications', 'Microprocessors and Microcontrollers', 'Digital System Testing and Testable Design', 'Database Management Systems', 'Distributed Systems', 'High Performance Computer Architecture', 'Logic for Computer Science', 'Database Engineering', 'Embedded Systems', 'Testing and Verification of Circuits', 'Cryptography and Network Security', 'Advances in Compiler Construction', 'Real Time Systems', 'Advanced Graph Theory', 'Theory of Programming Languages', 'Machine Learning', 'Low Power Circuits and Systems', 'Speech and Natural Language Processing', 'Object Oriented Systems', 'Formal Systems', 'Multimedia Systems', 'Advances in Digital and Mixed Signal Testing', 'Complex Networks', 'Information Retrieval', 'Information Theory and Coding', 'Error Control Coding', 'Fundamentals of information theory', 'Linear networking theory', 'linear and nonlinear circuits', 'network theory', 'Understanding UMAT radio networing modelling', 'ies gates psus networking theory', 'networking coding thoery', 'Building scalable networking servies', 'theories of communication networks', 'Silicon VLSI Technology', 'The Science and engineering of microelectronic fabrication', 'VLSI Technology', 'Technologies for VLSI packages', 'VLSI ceramic research and development', 'low power phase locked loop with multiple', 'VLSI Technology: fundamentals and Application', 'VLSI signal processing technologies', 'Discrete - time signal processing', 'Digital Signal processing', 'Theory and applications of digital signal processing', 'introduction of digital signal processing', 'digital signal processing: fundamentals and applications', 'digital signal processing: principals, algorithms', u"Schaum's outline of digital signal processing", 'digital signal processing techniques and applications', 'Introduction of computer science', 'Computer science question books', 'lectures notes in computer science', 'Graded problems in computer science', 'Algebra for computer science', 'Advance computer science', 'Computer science with C#', 'Probality with R: introduction with computer science', 'Century of electical engineering and computer scienceat MIT', 'Computer Science and scientific scoputing', 'Discrete structure of computer science', 'mathematics for computer science', 'Big data for dummies']

    matches = [x for x in books if re.search(find_book, x, re.M|re.I)]
    
    if len(matches)==0:
        speech="Not available"
    
    for i in matches:
        speech= speech + i + " , " 
        
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "python_stubot"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

app.run(debug=True, port=port, host='0.0.0.0')
