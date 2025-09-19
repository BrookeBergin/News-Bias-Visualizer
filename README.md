# News Bias Visualizer

### Try it here: https://news-bias-visualizer.onrender.com

### Images
![Website home screen](nbv/static/img/home-nbv.png)
<img src="nbv/static/img/immigration-nbv.png" alt="Graph results for immigration" width="45%">
<img src="nbv/static/img/election-nbv.png" alt="Graph results for election" width="45%">


## How It's Made:

**Languages:** Python, SQLite3, HTML, CSS
<br>**Frameworks:** Flask<br>
**Tools**: PyCharm, Github, Render

This personal project was developed during my moments of free time in August 2025. It was inspired by some of my classmates' final projects in my Spring 2025 "Natural Language Processing - Advanced Python" course at Georgetown University. My goal was to combine back-end nlp and data analysis skills (python and sqlite) with front-end design features (html, css) to develop a full-stack project with real-world importance.

### What does the tool accomplish?
The aim of the News Bias Visualizer (NBV) is to display bias differences across different mainstream U.S. news sources.

When the user inputs a keyword, the NBV finds all news articles published in 2016 containing that keyword. It calculates each source's [sentiment score](#what-is-the-sentiment-score) towards the word and plots these scores on the graph (averaging by month). The result is a graph that displays the degree of bias by each news source towards that word.

### Chosen limitations
Timeframe (2016): I chose 2016 because it was an impactful year in US politics and I theorized a greater display of news bias (cooler results). If I continued working on this proejct, I would increase the timeframe (and work on optimizing runtime)!

Location (USA): Simply put, I am American and I figure most users of this tool will be Americans. Adding sources from other countries and languages may be a place for later improvement.

Sources (New York Times, CNN, Fox, Washington Post): I chose mainstream, popular U.S. news sources that are a mix of left, right, and center-leaning.

### What is the sentiment score?
The NBV tool scores each word in relation to its context. It does so using NLTK SentimentIntensityAnalyzer.
Scores range from -1 to 1, where 1 is extreme positive sentiment, -1 is extreme negative, and 0 is neutral.

## Optimizations
To improve runtime efficiency, sentiment hash locally stores results for keywords on first search. Upon re-searching a keyword, the application reuses the previously-calculated data from the hash.

## Usage
1. This tool is deployed through Render. Click the link here, or paste it in your browser: https://news-bias-visualizer.onrender.com
   - Render may take time to load the application after long periods of inactivity. This is normal and expected.
2. Navigate to "try it" or "try the tool"
3. Enter a keyword and press submit.
   - When first entering a new word, it may take the tool up to 10 seconds to load.
4. View your graph!
