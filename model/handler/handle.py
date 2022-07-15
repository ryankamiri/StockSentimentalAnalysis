from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.stem import  SnowballStemmer
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from twilio.rest import Client
from dotenv import load_dotenv
import time
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import newsfilter

load_dotenv()

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
twilio = Client(account_sid, auth_token)

client = MongoClient(os.getenv('MONGO_URI'))
db=client.StockProject

stemmer = SnowballStemmer(language='english')

def preProcess(sentence):
    words = []
    for word in sentence.split():
        #Take out all non letter characters
        #word = re.sub("[^a-zA-Z]+", "", word.lower())
        word = word.lower()
        if word not in stopwords.words('english') and word != "":
            newWord = stemmer.stem(word)
            words.append(newWord.replace("'", ""))

    return ' '.join(words)

def createTokenizer(word_index, vocab_size=10000, oov_tok="<OOV>"):

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.word_index = word_index

    print(f"Word Index Size: {len(tokenizer.word_index)}")

    return tokenizer

def predict(headlines, tokenizer, model, max_length=35, trunc_type="post", padding_type="post",):
    for i in range(len(headlines)):
        headlines[i] = preProcess(headlines[i])
    
    sequences = tokenizer.texts_to_sequences(headlines)
    padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    return model.predict(padded)

with open("../models/word_index.json", "r", encoding="utf-8") as _file:
    word_index = json.load(_file)

tokenizer = createTokenizer(word_index)
model = tf.keras.models.load_model('../models/model.h5')

while True:
    headlines = newsfilter.getNews()

    toPredictHeadlines = []
    toPredictInfo = []
    for headline in headlines:
        exists = db.headlines.find_one({"url": headline["link"]})
        if not exists and len(headline["ticker"]) > 0 and headline["ticker"][0] != "":
            toPredictInfo.append(headline)
            toPredictHeadlines.append(headline["title"])
    
    if(len(toPredictHeadlines) <= 0):
        print("No new headlines found, Waiting 1 minute.")
        time.sleep(60)
        continue
    predictions = predict(toPredictHeadlines, tokenizer, model)

    newHeadlines = []
    for i in range(len(toPredictInfo)):
        info = toPredictInfo[i]
        sentiment = float(predictions[i][0])
        data = {
            'sentiment': sentiment,
            'headline': info["title"],
            'stocks': info["ticker"],
            'date': info["date"], 
            'url': info["link"]
        }
        newHeadlines.append(data)
        #db.headlines.insert_one(data)
        print(f'Added new headline {info["title"]}')
    db.headlines.insert_many(newHeadlines)
    print(f"Done adding {len(toPredictInfo)} new headlines, Handeling notifications.")

    #Handle notifcations
    messagesSent = 0
    for headline in newHeadlines:
        notifyUsers = db.users.find({"phoneNumber": {"$ne": None}, "$and": [{"notificationTarget": {"$ne": None}}, {"notificationTarget": {"$lte": headline['sentiment']}}]})
        for user in notifyUsers:
            #Text users
            phoneNumber = str(int(user["phoneNumber"]))
            twilio.messages.create(body=f"NEWS ALERT\n{headline['headline']}\nStocks: {','.join(headline['stocks'])}\nConfidence: {round(headline['sentiment'] * 100, 1)}%", from_=os.getenv("TWILIO_NUMBER"), to=phoneNumber)
            messagesSent += 1

    #Wait 1 minute
    print(f"Sent {messagesSent} SMS messages, Waiting 1 minute.")
    time.sleep(60)