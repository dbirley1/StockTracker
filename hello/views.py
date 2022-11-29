import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import StockForm
from plotly.offline import plot
from plotly.graph_objs import Scatter
import re
from . import stockAlg

# Raw Package
import numpy as np
import pandas as pd

# Market Data 
import yfinance as yf

#Graphing/Visualization
import datetime as dt 
import plotly.graph_objs as go 


def createChart(ticker):
    yf.pdr_override()

    # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
    df = yf.download(tickers=ticker,period='1d',interval='1m')

    stock_info = yf.Ticker(ticker).info
    currentTickerPrice = stock_info['regularMarketPrice']
    shortName = stock_info['shortName']
    print (str(stock_info))
    

    # Declare plotly figure (go)
    fig=go.Figure()

    

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    fig.update_layout(
        title= shortName + "(" + ticker + ") " +' Live Share Price: ' +  str(currentTickerPrice))              

    fig.update


    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return plot(fig, output_type='div', include_plotlyjs=False)

plot_div = createChart('^DJI')


def home(request):
    return render(request, "hello/home.html")

def stock(request):
    
    if request.GET.__contains__('ticker'):
        ticker=request.GET.__getitem__('ticker')
        if ticker != '':
            global plot_div
            plot_div = createChart(ticker),
            x = re.search("^\('.+',\)$", str(plot_div)),
            if (x):
                plot_div = re.sub("\('", "", str(plot_div), 1)
                plot_div = re.sub("',\)", "", str(plot_div))
        
    
    return render(request, 'hello/stock.html', context={'plot_div': plot_div})

def login(request):
    
    return render(request, "hello/login.html")

