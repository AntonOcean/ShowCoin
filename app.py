from flask import Flask
import requests
from flask import request, jsonify
import re
import os
from flask_sslify import SSLify


app = Flask(__name__)
sslify = SSLify(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        pattern = r'/\w+'
        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, str(price) + ' usd')
        return jsonify(r)
    return '<h1>Hello bot</h1>'


TOKEN = os.getenv('token_telegram_bot')
URL = f'https://api.telegram.org/bot{TOKEN}/'


def send_message(chat_id, text='Wait...'):
    url = URL + 'sendMessage'
    answer = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto


def get_price(crypto):
    url = 'https://api.coinmarketcap.com/v1/ticker{}'.format(crypto)
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    return price


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
