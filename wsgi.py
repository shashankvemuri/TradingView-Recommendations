from flask import Flask, request
import requests
from app.main import get_signal

app = Flask(__name__)

@app.route('/', methods=['GET'])
def func():
    ticker = request.args['ticker']
    interval = request.args['interval']
    return get_signal(ticker, interval)

if __name__ == "__main__":
    app.run()