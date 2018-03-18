# -*- coding:utf-8 -*-
"""
Author: Jingyuan Liu
Email: fdjingyuan@outlook.com
Project for competition 2018/3/11
"""

import urllib
import json
from flask import Flask
from flask import render_template, jsonify, request,make_response
import pyttsx3
from recognize import predict
import traceback
import uuid
import shutil

app = Flask(__name__)

### return html templates ###
@app.route('/')
def home():
    return render_template("front_page.htm")

@app.route('/reading')
def reading():
    return render_template("reading.html")


@app.route('/math')
def math():
    return render_template("math.html")





#begin of the voice
@app.route('/voice/<num>')
def voice(num):
    s = str(num)
    print(s)
    engine = pyttsx3.init()
    engine.say(s)
    engine.runAndWait()
    return jsonify({"Success":"Voice playing"})
#end of the voice


#begin of the recognize

@app.route('/recognize/', methods=['GET', 'POST'])
def rec():
    try:
        base64_data = request.get_data().strip()
        ret_num = int(predict(base64_data))
        print(ret_num)
        result = {
            'status': 'success',
            'data': ret_num
        }
    except Exception as e:
        result = {
            'status': 'error',

            'data': traceback.format_exc(),
        }
    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(debug=False)
