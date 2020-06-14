from flask import Flask, request, render_template
import requests
from app.main import get_signal

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ticker = request.form['ticker']
        interval = request.form['interval']
        return get_signal(ticker, interval)

    return render_template('home.html')
if __name__ == "__main__":
    app.run(debug=True)