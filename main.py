import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stocks_key = os.getenv("STOCKS_KEY")
news_key = os.getenv("NEWS_KEY")
# get stock information
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={stocks_key}'
stock_request = requests.get(url)
stock_data = stock_request.json()["Time Series (Daily)"]
print(stock_data)

yesterday = datetime.today().date() - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")
day_before_yesterday_str = day_before_yesterday.strftime("%Y-%m-%d")

yesterday_open_price = float(stock_data[yesterday_str]["1. open"])
daybfr_close_price = float(stock_data[day_before_yesterday_str]["4. close"])

percentage = (yesterday_open_price - daybfr_close_price) * 100 / yesterday_open_price
print(percentage)

message = None
if percentage >= 5.0:
    message = f"The open price is {percentage} higher than the day before close price"
elif percentage <= -5.0:
    message = f"The open price is {percentage} lower than the day before close price"

if message:  # then send the message
    # get top 3 articles about company
    news_url = "https://newsapi.org/v2/everything"
    parameters = {
        "q": COMPANY_NAME,
        "from": yesterday_str,
        "language": "en",
        "sortBy": "popularity",
        "apiKey": news_key
    }
    news_request = requests.get(news_url, params=parameters)
    news_data = news_request.json()
    top_news = []
    for index in range(0, 3):
        top_news.append(news_data["articles"][index])

    titles = [article["title"] for article in top_news]
    news_sources = [article["url"] for article in top_news]

    # send top 3 articles about that company
    from_phone_number = os.getenv("FROM_PHONE_NUMBER")
    to_phone_number = os.getenv("TO_PHONE_NUMBER")

    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="The most popular news about Tesla" \ 
             f"1.{titles[0]}\n{news_sources[0]}" \ 
             f"2.{titles[1]}\n{news_sources[1]}" \ 
             f"3.{titles[2]}\n{news_sources[2]}",
        from_=from_phone_number,
        to=to_phone_number,
    )
