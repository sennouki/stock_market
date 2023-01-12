import requests
import datetime as dt
from twilio.rest import Client
 
# DATE CONFIG
TODAY_INT = dt.date.today()
TODAY = str(TODAY_INT)
yesterday = TODAY_INT - dt.timedelta(days=1)
YESTERDAY = yesterday.isoformat()
DAY_B4 = TODAY_INT - dt.timedelta(days=2)
DAY_B4_Y = DAY_B4.isoformat()
 
# CONSTANTS
STOCK = "TSLA"
COMPANY_NAME = "TESLA INC"
STOCK_API_KEY = "###############"
STOCK_URL = "https://www.alphavantage.co/query?"
FUN = "TIME_SERIES_DAILY_ADJUSTED"
NEWS_API_KEY = "###############"
NEWS_URL = "https://newsapi.org/v2/everything?"
 
# REQUESTS
response = requests.get(f"{STOCK_URL}function={FUN}&symbol={STOCK}&apikey={STOCK_API_KEY}")
response.raise_for_status()
yesterday_stock = response.json()["Time Series (Daily)"][YESTERDAY]["4. close"]
day_b4_y_stock = response.json()["Time Series (Daily)"][DAY_B4_Y]["4. close"]
 
# CHECK DIFFERENCE
difference = float(yesterday_stock) - float(day_b4_y_stock)
percentage = round(difference / float(yesterday_stock) * 100)
 
# GET NEWS
if percentage >= 5 or percentage <= -5:
    news = requests.get(f"{NEWS_URL}q={COMPANY_NAME}&"
                        f"language=en&sortBy=popularityfrom={DAY_B4_Y}&to{YESTERDAY}&apiKey={NEWS_API_KEY}")
    news.raise_for_status()
    data = news.json()["articles"][:3]
    msg1 = data[0]["title"]
    msg2 = data[1]["title"]
    msg3 = data[2]["title"]
 
# SEND SMS
    account_sid = "###############"
    auth_token = "###############"
    client = Client(account_sid, auth_token)
    if percentage >= 5:
        message = client.messages.create(
            body=f'TSLA: 🔺{percentage}\n{msg1}\n{msg2}\n{msg3}',
            from_="###############",
            to="###############",
        )
 
        print(message.status)
    elif percentage <= -5:
        message = client.messages.create(
            body=f'TSLA: 🔻{percentage}\n{msg1}\n{msg2}\n{msg3}',
            from_="###############",
            to="###############",
        )
 
        print(message.status)
