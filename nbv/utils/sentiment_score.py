from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import wordpunct_tokenize

"""
takes any 1 article
scores the parts of the title that contain the keyword
"""
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

def score(article, keyword):
    try:
        nltk.data.find('sentiment/punkt_tab.zip')
    except LookupError:
        nltk.download('punkt_tab')

    # tokenize headline
    article_lines = sent_tokenize(article['title'])
    keyword = keyword.lower()

    # checks which lines contain keywords
    contains_keyword = []
    for line in article_lines:
        if keyword in wordpunct_tokenize(line.lower()):
            contains_keyword.append(line)
    if not contains_keyword:
        return None

    # score those lines and return compound (from -1 to 1)
    scores = [sid.polarity_scores(s)["compound"] for s in contains_keyword]
    return sum(scores) / len(scores)
