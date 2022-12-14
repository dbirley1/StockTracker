import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import loginForm
from plotly.offline import plot
from plotly.graph_objs import Scatter
import re
from . import stockAlg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import redirect, render

# Raw Package
import numpy as np
import pandas as pd

# Market Data 
import yfinance as yf

#Graphing/Visualization
import datetime as dt 
import plotly.graph_objs as go 

loginBool = False
globalUsername = ''


def createChart(ticker):
    yf.pdr_override()

    # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
    df = yf.download(tickers=ticker,period='1d',interval='1m')

    stock_info = yf.Ticker(ticker).info
    currentTickerPrice = stock_info['regularMarketPrice']
    try:
        shortName = stock_info['shortName']
    except:
        shortName = ''
 
    

    # Declare plotly figure (go)
    fig=go.Figure()

    

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    if shortName != '':
        fig.update_layout(
            title= shortName + "(" + ticker + ") " +' Live Share Price: ' +  str(currentTickerPrice))              
    else:
        fig.update_layout(title = 'INVALID TICKER HAS BEEN ENTERED. PLEASE TRY AGAIN')
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
    if loginBool == True:
        return render(request, 'hello/stock.html', {'plot_div': plot_div, 'username': globalUsername})
    else:
        return render(request, 'hello/stock.html', context={'plot_div': plot_div})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username = username, password = password)
    
        if user is not None:
            login(request, user)
            global loginBool
            loginBool = True
            global globalUsername
            globalUsername = username
            return redirect('stock')
        else:
            str = "Invalid Username or Password"
            return render(request, 'hello/login.html', context={'str':str} )
        
    return render(request, "hello/login.html")

def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirmPassword')

        user = User.objects.create_user(username,email,pass1)

        return redirect('/login')

    return render(request, "hello/register.html")

def user_logout(request):
    logout(request)
    return render(request, "hello/logout.html")

