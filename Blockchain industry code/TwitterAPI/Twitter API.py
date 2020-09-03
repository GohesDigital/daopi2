import twitter
import os
import tweepy as tw
import pandas as pd

# Our Gohes credentials
consumer_key = "Dh4wpl8xYCQLJRrUuP3NdBd5N"
consumer_secret = "9gIKq81n8O5dgFXWtXwyKfdJCndwKHWfvDMmhpOCp3x8FLm5ie"
access_token_key = "236269372-9DdKeCkVBMlZ5RZXgnZgR4bf16jpUTqBq4f332dd"
access_token_secret = "bI8kqIuNkTiZvYH893O4u7WkMVe1KyZ2LHMiJGIGKoxlE"

# Logging in using credentials
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Parameters, Search words and date since. Twitter API only allows 14 days of data. Cannot go further back.
search_words = "ICX"
date_since = "2020-08-30"

# Standard Loop to search in english tweets with max. item number
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(10)

# Iterate and print tweets
for tweet in tweets:
    print(tweet.text)
