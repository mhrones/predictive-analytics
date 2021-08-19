import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as spla
import pandas as pd
import praw
import datetime as dt

reddit = praw.Reddit(client_id='_iyJsafZdr_Oyg', \
                     client_secret='4Y8kkSLOe0d3GunMigVYAet2MYY', \
                     user_agent='top_news_scraper', \
                     username='hrones', \
                     password='irene1970')

sub_news = reddit.subreddit("news")

post_dictionary = { "title":[], \
                    "score":[], \
                    "url":[], \
                    "time created":[]}

for post in sub_news.top(limit=200):
    post_dictionary["title"].append(post.title)
    post_dictionary["score"].append(post.score)
    post_dictionary["url"].append(post.url)
    post_dictionary["time created"].append(post.created)


post_data = pd.DataFrame(post_dictionary)

print(post_data.title)
print(post_data.score)
print(post_data.url)

post_data.to_csv(r"C:\Users\matth\Documents\R\397A Homeworks\Homeworks\homework1\data.csv",index=False)
