# Stock and News Alert

This project retrieves stock data and news articles related to a specific company and sends an alert via SMS if there is a significant change in the stock price. The stock data is fetched from Alpha Vantage and news articles from NewsAPI. Twilio is used for sending SMS notifications.

## Features

- Retrieves daily stock data for a specified stock symbol.
- Calculates the percentage change in the stock price between yesterday and the day before.
- Retrieves the top 3 news articles about a specified company.
- Sends an SMS alert with the percentage change in stock price and the top news articles.

## Prerequisites

1. Python 3.x
2. Python libraries: `requests`, `twilio`
3. Environment variables for API keys and Twilio credentials
