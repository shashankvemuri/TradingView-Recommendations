from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def func():
    return render_template('app/template/home.html')

if __name__ == "__main__":
    app.run(debug=True)