import requests

def send_json(link = None, text = None):
    body = {
        'link': link,
        'text': text
    }
    myurl = 'http://127.0.0.1:8180/predict'
    headers = {'content-type': 'application/json; charset=utf-8'}
    response = requests.post(myurl, json=body, headers=headers)
    return response.json()['predictions']


link = 'https://lenta.ru/news/2022/04/21/tarpishev/'
predictions = send_json(link = link, text = None)
link = None

with open('files/test.txt', 'r') as f:
    text = f.read()
predictions = send_json(link = link, text = text)

print(predictions)