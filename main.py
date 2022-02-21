import yfinance as yf
import pandas as pd
import pandas_ta as ta
from discord_webhook import DiscordWebhook
import time
import datetime
import requests

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

#discordURL = "https://discord.com/api/webhooks/931120166069207051/xSDHrhxs6hdnqtDH52MSmVccxb5qsrbebtw1POr9Md1WQyLKLyB_Gocka_qTQdA3gG74"

#Find Chat id
#https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/getUpdates

#Chat in Trading bot grup
#requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-617694482&text={text}')

#Signals
#requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-717198200&text={text}')

#Vix trader
#requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')

# User input
chartPeriod = "600d"
interval = "1h"
emaLength1 = 400
buys = []
sells = []
inPosition = False
buyPrice = 0
sellPrice = 0
balance = 29004
percentage = None
leverage = 2

# Market data

prices = []
ema1 = []

df = pd.DataFrame()
df = df.ta.ticker("^VIX", period=chartPeriod, interval=interval)


def talk():
    global ema1
    global ema2
    price(prices, df)
    text = "Starting Vix trading bot with balance: " + str(balance)
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()
    text = "Current Vix price " + str(prices[-1])
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()
    text = "Current stategy buy vix under ema 400, sell when over ema 400 + 2"
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()
    text = "Status: Running..."
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()

def price(prices, df):
    print("Updating prices...")
    df = df.values.tolist()
    for i in range(len(df)):
        prices += [df[i][3]]

def EMA1(ema1, df):
    df = df.ta.ema(length=emaLength1)
    df = df.values.tolist()

    for i in range(len(df)):
        ema1 += [df[i]]

def lower(x, y):
    if x>y:
        return y
    else:
        return x

def objective(discord):
    global ema1
    global inPosition
    global buyPrice
    global sellPrice
    global discordURL
    global balance

    price(prices, df)
    EMA1(ema1, df)

    if inPosition:
        text = "Currently in position bought at: " + str(round(buyPrice, 2)) + "$ looking to sell at: " + str(round((ema1[-1] + 1), 2)) + "$, current price: " + str(round(prices[-1],2)) + "$, current balance: " + str(round(balance)) + "$, " + str(datetime.datetime.now())
    else:
        text = "Currently not in position, looking to buy back in at " + str(round(ema1[-1] - 1,2)) + "$, current price: " + str(round(prices[-1],2)) + "$, current balance: " + str(round(balance)) + "$, " + str(datetime.datetime.now())

    print(text)
    if discord:
        #DiscordWebhook(url=discordURL, content=text).execute()
        requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')


def trade(prices, ema1, percentage, leverage):
    global inPosition
    global buyPrices
    global balance
    global buyPrice
    global sellPrice

    if not inPosition:
        if prices[-1] < (ema1[-1] -1):
            #buy
            inPosition = True
            buyPrice = prices[-1]
            text = "Bought Vix at: " + str(round(buyPrice,2)) + "$"
            print(text)
            #DiscordWebhook(url=discordURL,content=text).execute()
            requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-717198200&text={text}')
            requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')
            text = "Looking to sell it back at: " + str(round((ema1[-1] + 1),2)) + "$"
            print(text)
            #DiscordWebhook(url=discordURL, content=text).execute()
            requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')
    else:
        if prices[-1] > (ema1[-1] + 1):
            #sell
            inPosition = False
            sellPrice = prices[-1]
            text = "Sold ^VIX at: " + str(round(sellPrice,2)) + "$"
            print(text)
            #DiscordWebhook(url=discordURL, content=text).execute()
            requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-717198200&text={text}')
            requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')
            text = "Looking to buy back in at: " + str(round((ema1[-1] - 1),2)) + "$"
            print(text)
            #DiscordWebhook(url=discordURL, content=text).execute()
            requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')
            percentage = ((sellPrice-buyPrice)/buyPrice*100)*leverage
            balance += balance*percentage/100
            text = "Gain/loss: " + str(round(percentage,1)) + "% With " + str(leverage) + "x leverage, current balance: " + str(round(
                balance)) + "$"
            print(text)
            #DiscordWebhook(url=discordURL,content=text).execute()
            requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')
            text = "-------------------------------------"
            #DiscordWebhook(url=discordURL, content=text).execute()

#talk()
counter = 200
while True:

    hora = int(str(datetime.datetime.now())[11:13])
    minuto = int(str(datetime.datetime.now())[14:16])
    print(hora,minuto)

    if hora == 15 and minuto == 45:
        text = "The Vix futures market just opened, happy trading!"
        requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')

    if hora == 22 and minuto == 15:
        text = "The market just closed, hope you printed some tendies"
        requests.get(f'https://api.telegram.org/bot5267223010:AAHpaQmvNWCEusnNRW86MmzHBpOeARfLPvE/sendMessage?chat_id=-777069776&text={text}')

    if ((hora == 15 and minuto >= 45) or hora >= 16) and hora < 23:
        df = df.ta.ticker("^VIX", period=chartPeriod, interval=interval)
        price(prices, df)
        EMA1(ema1, df)
        trade(prices, ema1, percentage, leverage)
        if counter > 12:
            counter = 0
            objective(True)
        else:
            objective(False)
        counter += 1
        time.sleep(240)
    else:
        print("Market is closed")
        counter = 200
    time.sleep(60)