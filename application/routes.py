import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from application import app
from flask import render_template, request, url_for, redirect, session
from application.Analyser.loadData import search, reddit_data, getSentiment
from application.Analyser.yfinance import yfinance_data
from application.forms import MyForm, AnalyzerForm
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pickle
from sqlalchemy import create_engine
import os
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

nltk.download('vader_lexicon')

# Make the graphs a bit prettier, and bigger
matplotlib.style.use(['seaborn-talk', 'seaborn-ticks', 'seaborn-whitegrid'])
plt.rcParams['figure.figsize'] = (15, 7)

conn_string = 'mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8'.format(
    user="Unnamed",
    password='RyMe/s67Jw4=',
    host='jsedocc7.scrc.nyu.edu',
    port=3306,
    db='unnamed',
    encoding='utf-8'
)
engine = create_engine(conn_string)
engine.execute('CREATE DATABASE IF NOT EXISTS unnamed')
engine.execute('USE unnamed')

def predictor(stock):
  stockdf = pd.read_sql("SELECT * FROM StockSentimentData", con=engine)
  stock_names = stockdf["Stocks"].tolist()
  predicted_stock_change = 0
  if stock in stock_names:
    loc = stock_names.index(stock)
  else:
    message = "Stock Not Available"
    return message
  X = stockdf[["Sentiment"]]
  Y = stockdf[["StockAVGDifference"]]
  reg = LinearRegression()
  reg.fit(Y, X)
  price_diff_pred = reg.predict(X)
  predicted_stock_change = price_diff_pred[loc][0]
  return predicted_stock_change

@app.route("/", methods=["GET", "POST"])
def index():
    session.pop('name', default=None)
    indexform = MyForm()
    if request.method == 'POST':
        if indexform.validate_on_submit():
            print(request.form['name'])
            session['name'] = request.form['name']
            return redirect(url_for("analyze"))
    return render_template("index.html", indexform=indexform)


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if not session.get("name") is None:
        name = session.get("name")
    else:
        name = "<i>'Random User'</i>"
    analyzerform = AnalyzerForm()
    analyzerform.stock.choices = ['AMC', 'NIO', 'AAPL', 'PLTR', 'GE', 'EDU', 'F', 'OCGN', 'BABA', 'AMD', 'FTEK', 'TSLA', 'WISH', 'BAC', 'ITUB', 'PALI', 'VALE', 'PLUG', 'IHT', 'UBER', 'FCX', 'RIOT', 'AAL', 'NOK', 'JD', 'MARA', 'PBR', 'X', 'GGB', 'BNGO', 'MSFT', 'INTC', 'XPEV', 'PTON', 'CCL', 'FCEL', 'T', 'FLR', 'TLRY', 'BBD', 'PFE', 'MRO', 'CLF', 'ET', 'XOM', 'DKNG', 'WFC', 'TME', 'SKLZ', 'NCLH', 'ARRY', 'IQ', 'SQ', 'OPEN', 'FUBO', 'RIG', 'VIAC', 'OXY', 'MU', 'ABEV', 'EXPR', 'SIRI', 'NNDM', 'AHT', 'C', 'FB', 'HBAN', 'RBLX', 'SOS', 'BA', 'SLB', 'SONO', 'M', 'WKHS', 'AMWL', 'CSCO', 'IDEX', 'CMCSA', 'KO', 'JPM', 'EBON', 'NLY', 'VIPS', 'FTCH', 'CPNG', 'SWN', 'TWTR', 'AMAT', 'PCG', 'NSA', 'SPCE', 'PINS', 'ZNGA', 'KGC', 'BB', 'KMI', 'GEVO', 'CCIV', 'UAL']
    return render_template("analyze.html", name=name, analyzerform=analyzerform)


@app.route("/result", methods=["POST"])
def result():
    if request.method == "POST":
        print(request.form)
        stock_input = request.form['stock']
        start_time_input = request.form['startDate']
        end_time_input = request.form['endDate']
        amountOfTweetsAndSubmissions = 20
        tweet_reddit_source_dict = {}
        day_num = int(end_time_input[-1]) - int(start_time_input[-1])
        tweet = search(stock_input, start_time_input, end_time_input, amountOfTweetsAndSubmissions)
        redditSub = reddit_data(stock_input, amountOfTweetsAndSubmissions)
        sent = []
        stock_data = yfinance_data(stock_input, day_num)
        sent_avg_list = []
        sent_avg = 0
        sent_avg_2 = 0
        sent_2 = []
        if tweet != None:
            for i in range(len(tweet)):
                sentiment = getSentiment(tweet[i])
                if isinstance(sentiment, int):
                    sent.append(sentiment)
                    sent_avg += sentiment
                else:
                    sentiment_score = sentiment["sentiment"]["document"]["score"]
                    sent.append(sentiment_score)
                    sent_avg += sentiment_score
                sent_avg = sent_avg / len(sent)
        sent_2 = []
        sent_avg_redd = 0
        if redditSub != None:
            for i in range(len(redditSub)):
                sentiment = getSentiment(redditSub[i])
                if isinstance(sentiment, int):
                    sent_2.append(sentiment)
                    sent_avg_redd += sentiment
                else:
                    sentiment_score = sentiment["sentiment"]["document"]["score"]
                    sent_2.append(sentiment_score)
                    sent_avg_redd += sentiment_score
        sent_avg_redd = sent_avg_redd / len(sent_2)
        total_avg = (sent_avg_redd + sent_avg) / 2
        if redditSub != None and tweet != None:
            tweet.extend(redditSub)
        tweet_reddit_source_dict["Twitter/Reddit Data"] = tweet
        sent.extend(sent_2)
        tweet_reddit_source_dict["Sentiment Compound Score"] = sent
        tweetDataframe = pd.DataFrame(tweet_reddit_source_dict)
        print(tweetDataframe)
        print("Predicted change in stock price:")
        print(predictor(stock_input))
        if total_avg > 0 and stock_data > 0:
            print("Positive Correlation") 
        elif total_avg < 0 and stock_data < 0:
            print("Negative Correlation") 
        else:
            print("No Correlation")
        return tweetDataframe.to_html()


def test():
    stock_input = "GME"
    start_time_input = "2021-05-09"
    end_time_input = "2021-05-09"
    amountOfTweetsAndSubmissions = 20
    tweet = search(stock_input, start_time_input,
                   end_time_input, amountOfTweetsAndSubmissions)
    redditSub = reddit_data(stock_input, amountOfTweetsAndSubmissions)
    sent = []
    # stock_data = main(stock_input, start_time_input, end_time_input)
    day_num = int(end_time_input[-1]) - int(start_time_input[-1])
    tweet_source_dict = {}
    stock_data = yfinance_data(stock_input, day_num)
    sent_avg_list = []
    stock_avg_diff_list = []
    sent_avg = 0
    sent_avg_2 = 0
    sent_2 = []
    if tweet != None:
        for i in range(len(tweet)):
            sentiment = getSentiment(tweet[i])
            if isinstance(sentiment, int):
                sent.append(sentiment)
                sent_avg += sentiment
            else:
                sentiment_score = sentiment["sentiment"]["document"]["score"]
                sent.append(sentiment_score)
                sent_avg += sentiment_score
        sent_avg = sent_avg / len(sent)
    sent_2 = []
    sent_avg_redd = 0
    if redditSub != None:
        for i in range(len(redditSub)):
            sentiment = getSentiment(redditSub[i])
            if isinstance(sentiment, int):
                sent_2.append(sentiment)
                sent_avg_redd += sentiment
            else:
                sentiment_score = sentiment["sentiment"]["document"]["score"]
                sent_2.append(sentiment_score)
                sent_avg_redd += sentiment_score
        sent_avg_redd = sent_avg_redd / len(sent_2)

    total_avg = (sent_avg_redd + sent_avg) / 2

    stock_avg_diff = 0
    for stock_diff in stock_data:
        stock_avg_diff += stock_diff
    stock_avg_diff = stock_avg_diff / len(stock_data)
    if redditSub != None:
        tweet.extend(redditSub)
    tweet_reddit_source_dict["Twitter/Reddit Data"] = tweet
    sent.extend(sent_2)
    tweet_reddit_source_dict["Sentiment Compound Score"] = sent
    tweetDataframe = pd.DataFrame(tweet_source_dict)
    tweetDataframe
    if total_avg > 0 and stock_avg_diff > 0:
        print("Positive Correlation")
    elif total_avg < 0 and stock_avg_diff < 0:
        print("Negative Correlation")
    else:
        print("No Correlation")
