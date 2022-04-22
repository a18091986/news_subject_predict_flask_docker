import json
import os
import dill
from flask import Flask, request, jsonify
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
from model_predict import model_predict


app = Flask(__name__)

model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route("/", methods=["GET"])
def general():
    return "Welcome to prediction process"


@app.route('/predict', methods=['POST'])
def predict():
    data = {"success": False}

    request_json = request.get_json()
    print(f'{"*" * 100}\n{request_json}\n{"*" * 100}')


    link, text = None, None

    if request_json["link"]:
        link = request_json['link']
        print('Поступила ссылка')

    if request_json["text"]:
        text = request_json['text']
        print('Поступил текст')

    print(f'{link}\n{text}')
    print('------------------------------------------------------------------------')

    try:
        preds = model_predict(link = link, text = text)
        data["predictions"] = preds.tolist()
        data["success"] = True

    except Exception as e:
        print(e)
        data["predictions"] = 0
        data['success'] = False
        print('test mode')
    # return the data dictionary as a JSON response
    return jsonify(data)
    return data


if __name__ == '__main__':

    port = int(os.environ.get('PORT', 8180))
    app.run(host = '0.0.0.0', debug=True, port = port)
