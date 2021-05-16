from polygon import RESTClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime
import praw
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import requests
import json
import pandas as pd
import nltk
import time
import sklearn
nltk.download('vader_lexicon')
# Make the graphs a bit prettier, and bigger
matplotlib.style.use(['seaborn-talk', 'seaborn-ticks', 'seaborn-whitegrid'])
plt.rcParams['figure.figsize'] = (15, 7)


def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')


def main(stock, start, end):
    key = "5tXFTr2GW77cTrgByzwl2ibeXbubesTh"

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        from_ = start
        to = end
        resp = client.stocks_equities_aggregates(
            stock, 1, "day", from_, to, unadjusted=False)

        #print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")
        diff_chart = []
        for result in resp.results:
            dt = ts_to_datetime(result["t"])
            diff = result['c'] - result['o']
            diff_chart.append(diff)
            #print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
    return diff_chart


payload = ""
headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOJVOAEAAAAAym0fsraKQD39gqqRzcG8n9mqffA%3D3MSxBpEwrMHl08PAAjNxIjy0AM8di31I9U7XXhIxT3WRgskHRM',
    'Cookie': 'guest_id=v1%3A161903049706096483; personalization_id="v1_4qcst6G485Yljpwma4VR3Q=="'
}


def search(query, start, end, max):
    starttime = str(start) + "T00:00:00Z"  # format :yr-mm-dd
    # format :yr-mm-dd, results are given in reverse chronological
    endtime = str(end) + "T00:00:00Z"
    maxresults = str(max)
    url = "https://api.twitter.com/2/tweets/search/recent?query=" + query + \
        "&start_time=" + starttime + "&end_time=" + \
        endtime + "&max_results=" + maxresults
    response = requests.get(url, headers=headers, data=payload)
    tweets = response.json()
    data = []
    if "data" in tweets:
        for i in range(len(tweets['data'])):
            data.append(tweets['data'][i]['text'])
        return data
    else:
        return None


def getSentiment(text):
    import requests
    import json
    try:
        sent = SentimentIntensityAnalyzer(text)
        return sent["compound"]
    except:
        endpoint = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
        username = "apikey"
        password = "yV0w0tQYFhAbgoJ0d-IMAtebL_5fdz-GRAvWzYb9bDa6"
        parameters = {
            'features': 'emotion,sentiment',
            'version': '2018-11-16',
            'text': text,
            'language': 'en',
        }
        resp = requests.get(endpoint, params=parameters,
                            auth=(username, password))
        return resp.json()


def reddit_data(stock_nam, num_subm):
    reddit_list = []
    reddit = praw.Reddit(
        client_id="G35gFCI_dmA9VQ",
        client_secret="Dfb4wf9ZKSsfErunvyrlq5LxIaHQvA",
        user_agent="This is J's first!",
    )
    subreddit = reddit.subreddit("wallstreetbets")
    for submission in subreddit.search(stock_nam, limit=num_subm):
        reddit_list.append(submission.title)
    if len(reddit_list) == 0:
        return None
    else:
        return reddit_list

# if __name__ == '__main__':
    # main()
