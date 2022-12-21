import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
import re

# Raw Package
import numpy as np
import pandas as pd

# Market Data 
import yfinance as yf

#Graphing/Visualization
import datetime as dt 
import plotly.graph_objs as go 

yf.__version__

class Stock:



    def __init__(self, ticker, plot_div=''):
        self.ticker = ticker
        self.plot_div = plot_div 
        

        yf.pdr_override()


        # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
        df = yf.download(tickers=ticker,period='1d',interval='1m')

        stock_info = yf.Ticker(ticker).info
        currentTickerPrice = stock_info['regularMarketPrice']
        shortName = stock_info['shortName']
        if 'longBusinessSummary' in stock_info:
            longBusinessSummary = stock_info['longBusinessSummary']
        else:
            longBusinessSummary = ''

        plot_div = self.createChart(ticker, df)

    def get_plotdiv(self):
        return self.plot_div
        


    def createChart(self, ticker, df):

        # Declare plotly figure (go)
        fig=go.Figure()



        fig.add_trace(go.Candlestick(x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'], name = 'market data'))

        fig.update_layout(
            title= "(" + ticker + ") " +' Live Share Price: ' )              

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