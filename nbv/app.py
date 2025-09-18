from flask import Flask, render_template, request
import os
from nbv.utils.init_db import *
from nbv.utils.insert_articles import *
from nbv.utils.plot_scores import *
from nbv.utils.sentiment_score import *
import sqlite3
from collections import defaultdict
import time
from datetime import datetime
import numpy as np
from nltk.stem import PorterStemmer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "instance", "news.db")
TEMPLATE_PATH = os.path.join(BASE_DIR, "nbv", "templates")

app = Flask(__name__, template_folder=TEMPLATE_PATH)
sentiment_hash = defaultdict(dict)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tool')
def tool():
    return render_template('tool.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    keyword = request.form['keyword']
    filtered_keyword = f"%{keyword}%"
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # create Articles if it doesn't exist
        exists = check_table_exists("Articles")
        if not exists:
            init_articles()

        # fill Articles if empty
        full = check_table_full("Articles")
        if not full:
            store_articles("../data/news_headlines_2016.csv")

        # confirm keyword not already in hash (optimize using local storage)
        if keyword not in sentiment_hash:
            # search for keyword in articles, store in local memory hash
            starttime = time.time()
            offset = 0
            batch_size = 20000
            while True:
                c.execute("SELECT id, title FROM Articles WHERE Title LIKE ? LIMIT ? OFFSET ?",
                          (filtered_keyword, batch_size, offset))
                batch = c.fetchall()
                if not batch:
                    break
                for article in batch:
                    article_score = score(article, keyword)
                    sentiment_hash[keyword][article['id']] = article_score
                offset += batch_size
            endtime = time.time()
            #print(sentiment_hash)
            print(f"Process completed in {endtime-starttime} seconds")
        # sort data by source
        data_points = []
        for article_id, sentiment in sentiment_hash[keyword].items():
            c.execute("SELECT source, published_at FROM Articles WHERE id = ?", (article_id,))
            row = c.fetchone()
            if row:
                source, published = row
                published_dt = datetime.fromisoformat(published)
                data_points.append((source, published_dt, sentiment))

        # group by source + week
        weekly_sentiment = defaultdict(lambda: defaultdict(list))
        for source, published, sentiment in data_points:
            week = published.strftime("%Y-%W")  # year-week string
            weekly_sentiment[source][week].append(sentiment)

        # average per week
        data_by_source = defaultdict(list)
        for source, week_dict in weekly_sentiment.items():
            for week, sentiments in week_dict.items():
                valid_sentiments = [s for s in sentiments if s is not None]
                if not valid_sentiments:
                    continue  # skip this week if all sentiments are None
                avg_sentiment = float(np.mean(valid_sentiments))
                data_by_source[source].append((week, avg_sentiment))


        plot_div = create_plot(data_by_source)

    return render_template('tool.html', graphJSON=plot_div, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)
