# Sentiment Analysis of tweets

In this Sentiment Analysis of Tweets project, I aim to analyze a large dataset of tweets and classify them based on sentiment. Leveraging machine learning techniques, I've trained a model to automatically determine whether a tweet expresses positive, negative, or neutral sentiment.

The project involves several steps, including data preprocessing, feature extraction, and model training. I've utilized natural language processing (NLP) techniques to clean and tokenize the text data, removing noise and irrelevant information.

# Table of contents:

- [Installation](#install)
- [Usage](#use)
- [Features](#features)
- [Technologies](#tech)
- [Demo Video](#video)
- [Live Demo](#demo)


<a id="install">
  
  # Installation:
  
  - Clone this project in the the directory.
  - Create a virtual environment in order to keep the project dependencies separate.
  - How ro create virtual environment?
      - Install virtualenv package in order to use it: `pip install virtualenv`
      - Create a new virtual env: `python<version> -m venv <virtual-environment-name>`
  - Install all requirements from requirements.txt file in order to run project: `pip install -r requirements.txt`
  - Open `SA_app.py` file and run it as a streamlit file using command: `streamlit run SA_app.py`.
  - Streamlit will run on the url something like `http://127.0.0.1:5000/`.
  - Navigate to that url and you will get the project interface.
  
<a id="use">
  
  # Usage:
  
  As mentioned, this project will guide you to analyse the tweets of any tweeter handle. See live demo mentioned below in order to understand usage in detail.

<a id="features">
  
  # Features:
  
  - You can fetch the tweets by just provideing the tweeter handle or keywords.
  - You can set the format to see data.
      - In the list format, you will get an option to copy the tweets.
  - Here, you can do the analysis of the tweets.
  - You can see the sentiment classification of all tweets (Positive, Neutral, Negative)
  - You will get an interactive bar graph of the above classification.
  - You will get the word cloud of the all tweets.
  - You will get an interactive line graph of sentiment analysis of tweets.
  - At last, you will get the scatterplot of polarity VS subjectivity.
  - You can download the data in csv format. The data contains following types.
      - **Type-1:** You will get a csv data of tweets, subjectivity, polarity, and analysis of all tweets.
      - **Type-2:** You will get a csv data of tweets, subjectivity, polarity, and analysis of all positive tweets.
      - **Type-3:** You will get a csv data of tweets, subjectivity, polarity, and analysis of all Neutral tweets.
      - **Type-4:** You will get a csv data of tweets, subjectivity, polarity, and analysis of all Negative tweets.

<a id="tech">
  
  # Technologies:
  
  The Car Price Prediction project utilizes the following technologies: 
  - **Python:** Python is a popular programming language for sentiment analysis due to its extensive libraries and frameworks for natural language processing (NLP) and machine learning.
  - **NLTK (Natural Language Toolkit):** NLTK is a widely used library in Python for NLP tasks. It provides various modules for tasks like tokenization, part-of-speech tagging, and sentiment analysis.
  - **TextBlob:** TextBlob is a Python library built on top of NLTK that offers a simple and intuitive API for common NLP tasks, including sentiment analysis.
  - **Data Visualization Libraries:** Libraries like Matplotlib, Seaborn, or Plotly can be used to visualize sentiment analysis results and present insights in a visually appealing manner.
  - **Streamlit:** Streamlit is an open-source Python library that allows you to create web applications and interactive data dashboards with minimal effort. It simplifies the process of building and deploying data-driven applications by providing an intuitive API and a straightforward development workflow.

<a id="video">
  
  # Demo Video
  
  Follow: https://www.youtube.com/watch?v=nj_eVMxFd58

<a id="demo">
  
  # Live Demo:
  
  Please follow https://sa-0t29.onrender.com/ in order to see the live demo of this project.
