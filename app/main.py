# imports 
import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask

'''
Intervals:
"1m" for 1 minute.
"5m" for 5 minutes.
"15m" for 15 minutes.
"1h" for 1 hour.
"4h" for 4 hours.
"1D" for 1 day.
"1W" for 1 week.
"1M" for 1 month.
'''

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

options = Options()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
webdriver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

# options = Options()
# options.add_argument("--headless")
# webdriver = webdriver.Chrome(executable_path='/Users/shashank/Documents/GitHub/StockRecommendations/chromedriver.exe', options=options)

app = Flask(__name__)
@app.route('/')
def get_signal(ticker, interval):
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
    line = '-'*50

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

    value = f'TradingView Data for {ticker} for {interval}: ' + '<br/>' + line + '<br/>' + f'Overall Signal: {signal}' + '<br/>' + f'Number of Sell Indicators: {num_sell}' + '<br/>' + f'Number of Neutral Indicators: {num_neutral}' + '<br/>' + f'Number of Buy Indicators: {num_buy}'
    return value