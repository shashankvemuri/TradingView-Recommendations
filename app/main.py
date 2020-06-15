# imports 
import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template
import yfinance as yf
import requests
from yahoo_fin import stock_info as si

# GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
# CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# options = Options()
# options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--no-sandbox")
# webdriver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

options = Options()
options.add_argument("--headless")
webdriver = webdriver.Chrome(executable_path='/Users/shashank/Documents/GitHub/Code/Finance/chromedriver.exe', options=options)

app = Flask(__name__)
@app.route('/')
def get_signal(ticker, interval):
    try:
        #Declare variable
        analysis = []

        #Open tradingview's site
        webdriver.get("https://s.tradingview.com/embed-widget/technical-analysis/?locale=en#%7B%22interval%22%3A%22{}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Afalse%2C%22height%22%3A%22100%25%22%2C%22symbol%22%3A%22{}%22%2C%22showIntervalTabs%22%3Atrue%2C%22colorTheme%22%3A%22dark%22%2C%22utm_medium%22%3A%22widget_new%22%2C%22utm_campaign%22%3A%22technical-analysis%22%7D".format(interval, ticker))
        webdriver.refresh()

        #Wait for site to load elements
        while len(webdriver.find_elements_by_class_name("speedometerSignal-pyzN--tL")) == 0:
            sleep(0.1)

        #Recommendation
        recommendation_element = webdriver.find_element_by_class_name("speedometerSignal-pyzN--tL")
        analysis.append(recommendation_element.get_attribute('innerHTML'))

        #Counters
        counter_elements = webdriver.find_elements_by_class_name("counterNumber-3l14ys0C")

        #Sell
        analysis.append(int(counter_elements[0].get_attribute('innerHTML')))

        #Neutral
        analysis.append(int(counter_elements[1].get_attribute('innerHTML')))

        #Buy
        analysis.append(int(counter_elements[2].get_attribute('innerHTML')))

        last_analysis = analysis
        signal = last_analysis[0]
        num_sell = last_analysis[1]
        num_neutral = last_analysis[2]
        num_buy = last_analysis[3]
        line = '-'*60

        company = yf.Ticker(ticker)
        company_name = company.info['longName']
        current_price = round(si.get_live_price(ticker), 2)

        if interval == "1m":
            long_interval = "1 minute"
        elif interval == "5m":
            long_interval = "5 minutes"
        elif interval == "15m":
            long_interval = "15 minutes"
        elif interval == "1h":
            long_interval = "1 hour"
        elif interval == "4h":
            long_interval = "4 hours"
        elif interval == "1D":
            long_interval = "1 day"
        elif interval == "1W":
            long_interval = "1 week"
        elif interval == "1M":
            long_interval = "1 month"

        ticker = ticker.strip('"')
        interval = interval.strip('"')
        line = line.strip('"')
        signal = signal.strip('"')

        ticker = json.dumps(ticker)
        interval = json.dumps(interval)
        signal = json.dumps(signal)
        num_sell = json.dumps(num_sell)
        num_neutral = json.dumps(num_neutral)
        num_buy = json.dumps(num_buy)
        line = json.dumps(line)

        return render_template('output.html', company_name = company_name, long_interval = long_interval, signal = signal, current_price = current_price, num_buy = num_buy, num_neutral = num_neutral, num_sell = num_sell)
    except Exception as e:
        return f"{e} <br> Sorry, this ticker or interval is unavailable"