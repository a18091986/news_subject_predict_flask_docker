from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField, IntegerRangeField, TextAreaField
from wtforms.validators import DataRequired
import requests
import json

class ClientDataForm(FlaskForm):

    link = StringField('link')
    text = TextAreaField('text')


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(link, text):
    body = {'link': link,
            'text': text}

    myurl = 'http://127.0.0.1:8180/predict'
    headers = {'content-type': 'application/json; charset=utf-8'}
    response = requests.post(url = myurl, json=body, headers=headers)
    return response.json()['predictions']


@app.route("/")
def index():
    return render_template('index_.html')


@app.route('/predicted_/<response>')
def predicted(response):
    response = json.loads(response)
    return render_template('predicted_.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['link'] = request.form.get('link')
        data['text'] = request.form.get('text')


        print(f'{"*" * 100}\n{data["text"]}\n{"*" * 100}')

        try:
            response = get_prediction(data['link'], data['text'])
            response = str([round(x,2)*100 for x in response])

        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})

        return redirect(url_for('predicted', response=response))
    return render_template('form_.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
