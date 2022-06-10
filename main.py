from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

def stockInfo(sym):
    sym = str(sym).lower()
    tickr = yf.Ticker(sym)
    closePlot(tickr)
    earningPlot(tickr)
    properties = ['open','dayHigh','dayLow','fiftyTwoWeekLow','fiftyTwoWeekHigh','dividendYield','pegRatio','marketCap','longName','logo_url']
    tickr_dict = tickr.info
    props_dict = {}
    for prop in properties:
        props_dict[prop] = tickr_dict[prop]
    return props_dict


def earningPlot(ticker):
    ticker_hist = ticker.history(start="2022-01-01", end="2022-07-01", interval="1mo")
    sr = ticker_hist.Close
    closes = [close[1] for close in sr.iteritems() if not np.isnan(close[1])]
    percentages = []
    previous = None
    for close in closes:
        if previous == None:
            previous = close
            continue
        else:
            instance = ((previous - close)/close) * 100
            percentages.append(instance)
            previous = close
    date = [str(close[0])[:10] for close in sr.iteritems() if (not np.isnan(close[1])) ]
    plt.bar(date[1:], percentages)
    plt.savefig('static/earningplot.png')
    plt.close()

def closePlot(ticker):
    ticker_hist = ticker.history(start="2022-01-01")
    sr = ticker_hist.Close
    closes = [close[1] for close in sr.iteritems() if not np.isnan(close[1])]
    date = [str(close[0])[:10] for close in sr.iteritems() if (not np.isnan(close[1])) ]
    plt.plot(date, closes, linewidth=2.0)
    plt.xticks([])
    plt.rcParams["figure.figsize"] = (10,5)
    plt.savefig("static/closeplot.png")
    plt.close()

@app.route("/",methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        data = {'response' : request.form['symbol']}
        stock_data = stockInfo(data['response'])
        return render_template("dashboard.html",stock_data=stock_data, symbol = data["response"])
    stock_data = stockInfo('aapl')
    return render_template("dashboard.html",stock_data=stock_data, symbol = "aapl")

if __name__ == '__main__':
    app.debug = True
    app.run()
