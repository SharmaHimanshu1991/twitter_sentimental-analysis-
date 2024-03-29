import sys
import csv
import tweepy
import matplotlib.pyplot as plt
from textblob import  TextBlob

from collections import Counter
#from aylienapiclient import textapi

if sys.version_info[0] < 3:
   input = raw_input

## Twitter credentials
consumer_key = "m1KhQXmdpmKRt8bd79XOQsagy"
consumer_secret = "Hk5Cq3CuxjHoPU1gSxz9IIUk9ff8dPYi2mr5Dtz6tBoDLTmEhy"
access_token = "2196107940-7L6HZ7715GQNWqVerKd3nSQefU6aMFp2HyUBbuM"
access_token_secret = "QE8MRGXbZp7RHxZP5eCqrDaPaNW6sNTSB3k0Zrb4TayBD"
'''
## AYLIEN credentials
application_id = "Your app ID here"
application_key = "Your app key here"
'''
## set up an instance of Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
'''
## set up an instance of the AYLIEN Text API
client = textapi.Client(application_id, application_key)
'''

## search Twitter for something that interests you
query = input("What subject do you want to analyze for this example? \n")
number = input("How many Tweets do you want to analyze? \n")

results = api.search(q=query , count=number)
#results = api.search(lang="en",  q=query + " -rt", count=number, result_type="recent")

print("--- Gathered Tweets \n")

## open a csv file to store the Tweets and their sentiment 
file_name = 'Sentiment_Analysis_of_Tweets_About.csv'.format(number, query)

with open(file_name, 'w') as csvfile:
   csv_writer = csv.DictWriter(
       f=csvfile,
       fieldnames=["Tweet", "Sentiment"]
   )
   csv_writer.writeheader()

   print("--- Opened a CSV file to store the results of your sentiment analysis... \n")

## tidy up the Tweets and send each to the AYLIEN Text API
   for c, result in enumerate(results, start=1):
       tweet = result.text
       client= TextBlob(tweet)
       #tidy_tweet = tweet.strip().encode('ascii', 'ignore')

       if len(tweet) == 0:
           print('Empty Tweet')
           continue
       
       #response = client.sentiment
      
       #response = client.sentiment({'text': tidy_tweet})
       response = client.sentiment({'text': tweet})

       
       csv_writer.writerow({
           'Tweet': response['text'],
           'Sentiment': response['polarity']
       })
      
       print("Analyzed Tweet {}".format(c))
      
## count the data in the Sentiment column of the CSV file 
with open(file_name, 'r') as data:
   counter = Counter()
   for row in csv.DictReader(data):
       counter[row['Sentiment']] += 1

   positive = counter['positive']
   negative = counter['negative']
   neutral = counter['neutral']

## declare the variables for the pie chart, using the Counter variables for "sizes"
colors = ['green', 'red', 'grey']
sizes = [positive, negative, neutral]
labels = 'Positive', 'Negative', 'Neutral'

## use matplotlib to plot the chart
plt.pie(x=sizes,shadow=True,colors=colors,labels=labels, startangle=90)

plt.title("Sentiment of {} Tweets about {}".format(number, query))
plt.show()
