from flask import Flask, request, render_template
import requests
from app.main import get_signal

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/recommendation', methods=['POST'])
def func():
     ticker = request.form['ticker']
     interval = request.form['interval']
     return get_signal(ticker, interval)

if __name__ == "__main__":
    app.run(debug=True)