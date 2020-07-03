from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt
import urllib3

WordList = []



def percentage(part, whole):
    return 100 * float(part)/float(whole)


def put_in_file():
    global WordList
    file_name = searchTerm + '.txt'
    for word in WordList:
        with open(file_name, "a+", encoding="utf-8") as f:
            f.write(word)


def word_count(string):
    counts = dict()
    words = string.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return len(counts)


def search_item(search_term, next=False, page=0):
    if next == False:
        page = requests.get("https://www.nairaland.com/search?q=" + urllib3.parse.quote_plus(str(search_term)) )
    else:
        page = requests.get("https://www.nairaland.com/search/"
                            + str(search_term) + "/0/" + str(page))
    soup = BeautifulSoup(page.content, 'html.parser')

    comments = soup.findAll("div", {"class": "narrow"})

    return comments


def add_to_word_list(strings):
    global WordList
    k = 0
    while k < len(strings):
        if word_count(strings[k].text) > 1:
            WordList.append(strings[k].text)
        k += 1


searchTerm = input("Enter search term: ")


j = 0

while j < 20:
    if j == 0:
        nextItem = False
    else:
        nextItem = True
    commentsCurrent = search_item(searchTerm, nextItem, j)
    add_to_word_list(commentsCurrent)
    j += 1

polarity = 0
positive = 0
negative = 0
neutral = 0


put_in_file()

previous = []

for tweet in WordList:
    if tweet in previous:
        continue
    previous.append(tweet)
    analysis = TextBlob(tweet)
    #print(analysis.sentiment)
    polarity += analysis.sentiment.polarity

    if (analysis.sentiment.polarity == 0):
        neutral += 1
    elif (analysis.sentiment.polarity < 0.00):
        negative += 1
    elif (analysis.sentiment.polarity > 0.0):
        positive += 1

noOfSearchTerms = positive + negative + neutral


positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)

positive = format(positive, '.2f')
neutral = format(neutral, '.2f')
negative = format(negative, '.2f')

print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " comments from "
        "on nairaland")

if (polarity == 0):
    print("Neutral")
elif (polarity < 0):
    print("Negative")
elif (polarity > 0):
    print("Positive")

app = Flask(__name__)
@app.route("/")
def result():

    return jsonify( {"positive(%)" : positive},
                    {"neutral(%)" : neutral},
                    {"negative(%)" : negative},
                    
    
    
    
    )



# labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
# sizes = [positive, neutral, negative]
# colors = ['yellowgreen', 'gold', 'red']
# patches, texts = plt.pie(sizes, colors=colors, startangle=90)
# plt.legend(patches, labels, loc="best")
# plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' comments '
#                                                                                                  'on nairaland.')
# plt.axis('equal')
# plt.tight_layout()
# plt.show()
# exit() 
