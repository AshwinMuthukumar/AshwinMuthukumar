import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
from flask import Flask,request,render_template,redirect
from flair.models import TextClassifier
from flair.data import Sentence

app = Flask(__name__,static_url_path="",static_folder="static")
class DataStore():
    data = None
    limit = None
    query = None
getdata = DataStore()




classifier = TextClassifier.load('en-sentiment')
def get_sentiment(tweet):
    sentence = Sentence(tweet)
    classifier.predict(sentence)
    text = [sentence.labels[0].value,round(float(sentence.labels[0].score),2)]
    try:
        return text
    except:
        return 0

def preprocess_text(text):

    text = text.lower()
    text = re.sub("@[\w]*", "", text)
    text = re.sub("#[\w]*", "", text)
    text = re.sub("http\S+", "", text)
    text = re.sub("[^a-zA-Z#]", " ", text)
    text = re.sub("rt", "", text)
    text = re.sub("\s+", " ", text)
    return text

headings = ("Date","User","Tweet")

@app.route('/')
def result_():
    return render_template("Homepage.html")

@app.route('/Homepage',methods = ["GET","POST"])
def Home():
    return render_template("Homepage.html")

@app.route('/Guide',methods = ["GET","POST"])
def guide():
    return render_template("Guide.html")

@app.route('/About',methods = ["GET","POST"])
def about():
    return render_template("About.html")

@app.route('/result',methods = ["POST"])

def apii():
    query=request.form["search"]

    try:
        limit = int(request.form["limit"])
    except:
        limit = 100

    tweets = []
    cal = 0
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():

        if len(tweets) == limit:
                break

        else:
            
            tweets.append([tweet.date ,tweet.username, tweet.content])
    df1 = pd.DataFrame(tweets, columns=['Date','User', 'Tweet'])
    data = df1.values.tolist()
   
    i = 0

    while i < len(tweets):

            original_tweet = str(tweets[i])
            clean_tweet = preprocess_text(original_tweet)
            sentiment = round(get_sentiment(clean_tweet),2)
            positive = None
            negative = None
            
            if sentiment[0]=="POSITIVE":
                positive = sentiment[1]*100
                negative = 100 - positive
            else:
                negative = sentiment[1]*100
                positive = 100-sentiment[1]*100


    getdata.data = data
    getdata.query = query

    return render_template("chart.html",positive = positive, negative=negative,limit=limit,data=data,headings=headings,query=query)


@app.route('/Tweets' ,methods = ["GET","POST"])

def TweetTable():
    data = getdata.data
    try:
        return render_template('Tweets.html',headings=headings,data = data)
    except:
        return render_template('http://127.0.0.1/')

@app.route('/News' ,methods = ["GET","POST"])

def news():
    query = getdata.query
    return redirect("https://www.google.com/search?q="+query+"&rlz=1C1YTUH_enIN1024IN1024&sxsrf=AJOqlzVWl0FwgdQ8V44FclQxMF11malSaQ:1675585119320&source=lnms&tbm=nws&sa=X&ved=2ahUKEwi5vs_--P38AhW3XWwGHcboAnAQ_AUoAXoECAEQAw&cshid=1675585125344787&biw=1920&bih=937&dpr=1")



app.run(host= "0.0.0.0" , port= 80, debug=True)

