import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import scipy.linalg as spla
import pandas as pd
import praw
import datetime as dt
import string

reddit = praw.Reddit(client_id='_iyJsafZdr_Oyg', \
                     client_secret='4Y8kkSLOe0d3GunMigVYAet2MYY', \
                     user_agent='top_news_scraper', \
                     username='hrones', \
                     password='irene1970')

sub_news = reddit.subreddit("politics")

post_dictionary = { "title":[], \
                    "author":[], \
                    "score":[], \
                    "url":[], \
                    "time created":[]}

for post in sub_news.top(limit=300):
    post_dictionary["title"].append(post.title)
    post_dictionary["score"].append(post.score)
    post_dictionary["url"].append(post.url)
    post_dictionary["time created"].append(post.created)
    post_dictionary["author"].append(post.author)

post_data = pd.DataFrame(post_dictionary)

"""
Finding Author Frequency
"""

author_frequency = {}

for auth in post_dictionary["author"]:
    if(auth in author_frequency):
        author_frequency[auth] += 1
    else:
        author_frequency[auth] = 1

auth_freq_sorted = {key: val for key, val in sorted(author_frequency.items(), key = lambda ele: ele[1], reverse = True)}

auth_freq_sorted_df = pd.DataFrame(auth_freq_sorted, index=[0])

username_strings = []
t= 0
for user in auth_freq_sorted.keys():
    username_strings.append(str(t))
    t += 1



plt.bar(username_strings, auth_freq_sorted.values())
plt.ylabel("Frequency of Creators")
plt.xlabel("Creators of Top Posts Sorted in Descending Order ")
plt.xticks(rotation = "vertical")
plt.tick_params(axis = 'x', which = 'minor', labelsize = 3)
plt.savefig('author_freq_bar_graph.pdf')

plt.show()

"""
End Author Frequency
"""
"""
Finding URL Frequency
"""

site_freq = {}

for url in post_dictionary["url"]:
    # Cutting off 'https:\\'
    url_string = url[8:]

    # checking to see if the link contains a 'www.'
    possible_www = url_string[0:4]      # if the link has a 'www.' it will be in this substring
    if possible_www == "www.":          # checking to see if substring is 'www.'
        url_string = url_string[4:]     # if it is then the new url_string is created, one without a 'www.'

    # finding where the site identifier ends
    dot_index = 0
    for i in range(len(url_string)):
        if url_string[i] == ".":
            dot_index = i
            break
        else:
            continue
        break

    site_name = url_string[:dot_index]  # cutting the string down to only its site identifier

    if(site_name in site_freq):
        site_freq[site_name] += 1
    else:
        site_freq[site_name] = 1

site_freq_sorted = {key: val for key, val in sorted(site_freq.items(), key = lambda ele: ele[1], reverse = True)}


plt.bar(site_freq_sorted.keys(), site_freq_sorted.values())
plt.ylabel("Frequency of News Site")
plt.xlabel("Sites Featured in Top Posts Sorted in Descending Order ")
plt.xticks(rotation = "vertical")
plt.tick_params(axis = 'x', which = 'minor', labelsize = 3)
plt.savefig('site_freq_bar_graph.pdf')
plt.show()

"""
End URL Frequency
"""

"""
Finding Word Cloud
"""

p = [".", "?", "!", ",", ";", ":", "|" , "'" , "'"]
space = [""]*8

words = []
str = str(post_dictionary["title"])

exclude = set(string.punctuation)
str = ''.join(ch for ch in str if ch not in exclude)


words = str.split()

print(words)

for word in words:
    if "\u2015" in word:
        words.remove(word)

wordcloud = WordCloud(width=1920, height=1080, background_color="white").generate(str)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('titles_wordcloud.pdf')
plt.show()

"""
Plotting posts that contain the word trump
"""

categories = {}
says_trump = []
no_trump = []
trump_scores = []
no_scores = []

titles = post_dictionary["title"]
scores = post_dictionary["score"]

for title, score in zip(titles, scores):
    lower_title = title.lower()
    if( "trump" in lower_title):
        says_trump.append(title)
        trump_scores.append(score)
        categories[title] = "red"
    else:
        no_trump.append(title)
        no_scores.append(score)
        categories[title] = "blue"


data = (trump_scores, no_scores)
colors = ("red","blue")
groups = ("Contains 'Trump'", "Doesn't Contain 'Trump'")

trimmed_trump_titles = []

for title in says_trump:
    inter = title[:25]
    inter.join("....")
    trimmed_trump_titles.append(inter)

says_trump = trimmed_trump_titles

trimmed_no_titles = []

for title in no_trump:
    inter = title[:25]
    inter.join("....")
    trimmed_no_titles.append(inter)

no_trump = trimmed_no_titles

print(categories)

plt.scatter(titles[:-1], scores[:-1], alpha=0.8, c=categories.values(), edgecolors='none', s=30, label="Says trump")
plt.title('Scatter Plot')
plt.xlabel('x')
plt.xticks(rotation = "vertical")
plt.tick_params(axis = 'x', which = 'minor', labelsize = 3)
plt.ylabel('y')
plt.savefig('scatter_plot.pdf')
plt.show()


"""

Creating graphs to represent our data

1. Frequency at which news sites appear             (BAR GRAPH)
2. Score vs Creation Time                           (SCATTER PLOT)
3. Frequency at which certain authors appear        (BAR GRAPH)
4. Word Cloud                                       (LINE GRAPH)

"""
post_data.to_csv("data.csv",index=False)
