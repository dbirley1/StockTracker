import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import StockForm
from plotly.offline import plot
from plotly.graph_objs import Scatter

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

    print(df)

    # Declare plotly figure (go)
    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    fig.update_layout(
        title= ticker+' Live Share Price:',)               

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return plot(fig, output_type='div', include_plotlyjs=False)

plot_div = createChart('AMZN')


def home(request):
    return render(request, "hello/home.html")

def stock(request):
    
    if request.GET.__contains__('ticker'):
        ticker=request.GET.__getitem__('ticker')
        global plot_div
        plot_div = createChart(ticker),

    return render(request, 'hello/stock.html', context={'plot_div': plot_div})

def contact(request):
    
    return render(request, "hello/contact.html")

def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )