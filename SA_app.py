# Import the libraries
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import time
import plotly.graph_objects as go
import plotly.express as px
import base64


class Authentication:
    def auth(self):
        file = open('details.json',)
        file_data = json.load(file)
        api_key = file_data['API_Key']
        api_key_secret = file_data['API_kay_secret']
        Bearer_Token = file_data['Bearer_Token']
        accessToken = file_data['accessToken']
        accessTokenSecret = file_data['accessTokenSecret']
        # Create the authentication object
        authenticate = tweepy.OAuthHandler(api_key, api_key_secret)

        # Set the access token and access token secret
        authenticate.set_access_token(accessToken, accessTokenSecret)

        # Create the API object while passing in the auth information
        api = tweepy.API(authenticate, wait_on_rate_limit=True)
        return api

# function to clean the tweets
def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)   # Remove @mentions
    text = re.sub(r'#', '', text)               # Remove '#' symbol
    text = re.sub(r'RT[\s]+', '', text)         # Remove RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyperlinks
    text = re.sub(r'\n+', '', text) 
    return text

# Create a function to get the subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# Create a function to compute the ngative, neutral, and positive analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


# -------------------------------------------------------------------------------------------------

st.title('Sentiment Analysis Platform 📈')











sidebar = st.sidebar.radio(
    "Select the feature",
    ('See Tweets', 'Sentiment Analysis Of Tweets', 'See Data'),
)
st.sidebar.markdown('<hr><br><b>--------------------- Created by <a href="https://omkarsantoshraut.github.io/OmkarRaut/" target="_blank">Omkar Raut</a>.</b>', True)

if sidebar == 'See Tweets':
    st.markdown('<hr>', True)
    st.header('Functions of this tab:')
    st.write('1. You can fetch the tweets by just provideing the tweeter handle or keywords.')
    st.write('2. You can set the format to see data.')
    st.write('3. In the list format, you will get an option to copy the tweets.')
    st.markdown('<hr>', True)


    st.header('Provide inputs:')
    authenticate = Authentication()
    api = authenticate.auth()
    tweeterHandle = st.text_input('Enter tweeter handle or any keyword to see the tweets (Without @)')
    number = st.number_input('How many recent tweets you want to see (max=200)?', value=10, min_value=1, max_value=200)
    tableorlist = st.radio('Select the view to display tweets', ('Table', 'List'))
    see_btn = st.button('See Tweets')

    if tweeterHandle and number:
        try:
            posts = api.user_timeline(screen_name = tweeterHandle, count=number, tweet_mode = "extended")
            posts_df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])
        except:
            st.error('Fill all details and press the "See Tweets" button to see the tweets.')
    
    if see_btn and tableorlist == 'Table':
        st.markdown('<hr>', True)
        try:
            st.table(posts_df)
        except:
            st.error('Fill all details and press the "See Tweets" button to see the tweets.')
    elif see_btn and tableorlist == 'List':
        st.markdown('<hr>', True)
        try:
            st.write(posts_df['Tweets'].values.tolist())
        except:
            st.error('Fill all details and press the "See Tweets" button to see the tweets.')
    else:
        st.markdown('<hr>', True)
        st.info('Fill all details and press the "See Tweets" button to see the tweets.')
        

elif sidebar == 'Sentiment Analysis Of Tweets':
    st.markdown('<hr>', True)
    st.header('Functions of this tab:')
    st.write('1. Here, you can do the analysis of the tweets.')
    st.write('2. You can see the sentiment classification of all tweets (Positive, Neutral, Negative)')
    st.write('3. You will get an interactive bar graph of the above classification.')
    st.write('4. You will get the word cloud of the all tweets.')
    st.write('5. You will get an interactive line graph of sentiment analysis of tweets.')
    st.write('6. At last, you will get the scatterplot of polarity VS subjectivity.')
    st.markdown('<hr>', True)
    st.header('Provide inputs:')


    authenticate = Authentication()
    api = authenticate.auth()
    tweeterHandle = st.text_input('Enter tweeter handle or any keyword to see the tweets (Without @)')
    number = st.number_input('How many recent tweets you want to analyse?', value=100, min_value=1, max_value=200)
    ana_btn = st.button('Do Analysis')


    if ana_btn and number and tweeterHandle:
        posts = api.user_timeline(screen_name = tweeterHandle, count=number, tweet_mode = "extended")
        posts_df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])
        alltweets = ' '.join([twts for twts in posts_df['Tweets']])
        posts_df['Tweets'] = posts_df['Tweets'].apply(cleanTxt)
        posts_df['subjectivity'] = posts_df['Tweets'].apply(getSubjectivity)
        posts_df['polarity'] = posts_df['Tweets'].apply(getPolarity)
        posts_df['Analysis'] = posts_df['polarity'].apply(getAnalysis)
        
        st.markdown('<hr>', True)
        st.write('Tweets classifications (Positive, Neutral, Negative)')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tweets", str(len(posts_df)), "100%")
        col2.metric("Positive Tweets", str(len(posts_df[posts_df['polarity'] > 0])), "{:.2f}".format((len(posts_df[posts_df['polarity'] > 0])*100/len(posts_df)))+"%")
        col3.metric("Neutral Tweets", str(len(posts_df[posts_df['polarity'] == 0])), "{:.2f}".format(len(posts_df[posts_df['polarity'] == 0])*100/len(posts_df))+"%")
        col4.metric("Negative Tweets", str(len(posts_df[posts_df['polarity'] < 0])), "{:.2f}".format(len(posts_df[posts_df['polarity'] < 0])*100/len(posts_df))+"%")
        st.markdown('<hr>', True)

        fig = go.Figure([go.Bar(x=['Positive', 'Neutral', 'Negative'], y=[len(posts_df[posts_df['polarity'] > 0]), len(posts_df[posts_df['polarity'] == 0]), len(posts_df[posts_df['polarity'] < 0])])])
        fig.update_layout(
            yaxis_title = 'Number of tweets',
            title='Visualization of classification of '+str(len(posts_df))+" tweets using bar graph.",
            margin=dict(l=0, r=0, b=0),
        )
        st.plotly_chart(fig)
        st.markdown('<hr>', True)

        st.write('Word cloud of the fetched tweets:')
        word_cloud = WordCloud(collocations = False, background_color = 'white').generate(alltweets)
        st.image(word_cloud.to_array())
        st.markdown('<hr>', True)

        fig = go.Figure(data=go.Scatter(x=posts_df.index.tolist(), y=posts_df['polarity'].values.tolist(), mode='markers+lines'))
        fig.update_layout(
            xaxis_title='Tweet Number',
            yaxis_title = 'Polarity (Positive/Neutral/Negative)',
            title='Sentiment Analysis of the tweets'
        )
        st.plotly_chart(fig)
        st.markdown('<hr>', True)

        fig = px.scatter(posts_df, x="polarity", y="subjectivity", color="Analysis", symbol="Analysis")
        fig.update_layout(title='Polarity VS Subjectivity Scatterplot.')
        st.plotly_chart(fig)

    else:
        st.markdown('<hr>', True)
        st.info('Fill all details and press the "Do Analysis" button.')

else:
    st.markdown('<hr>', True)
    st.header('Functions of this tab:')
    st.write('1. You can download the data in csv format. The data contains following types.')
    st.write('2. Type-1: You will get a csv data of tweets, subjectivity, polarity, and analysis of all tweets.')
    st.write('3. Type-2: You will get a csv data of tweets, subjectivity, polarity, and analysis of all positive tweets.')
    st.write('4. Type-3: You will get a csv data of tweets, subjectivity, polarity, and analysis of all Neutral tweets.')
    st.write('5. Type-4: You will get a csv data of tweets, subjectivity, polarity, and analysis of all Negative tweets.')
    st.markdown('<hr>', True)
    st.header('Provide inputs')

    authenticate = Authentication()
    api = authenticate.auth()
    tweeterHandle = st.text_input('Enter tweeter handle or any keyword to get the tweets (Without @)')
    number = st.number_input('How many recent tweets and data you want to see (max = 200)?', value=10, min_value=1, max_value=200)
    data_btn = st.button('Get Data')

    if tweeterHandle and number and data_btn:
        posts = api.user_timeline(screen_name = tweeterHandle, count=number, tweet_mode = "extended")
        posts_df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])
        posts_df['Tweets'] = posts_df['Tweets'].apply(cleanTxt)
        posts_df['subjectivity'] = posts_df['Tweets'].apply(getSubjectivity)
        posts_df['polarity'] = posts_df['Tweets'].apply(getPolarity)
        posts_df['Analysis'] = posts_df['polarity'].apply(getAnalysis)

        st.markdown('<hr>', True)
        st.write('Data with all polarities')
        st.dataframe(posts_df)
        csv = posts_df.to_csv().encode()
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="All_data.csv" target="_blank">Download csv file</a>'
        st.markdown(href, unsafe_allow_html=True)

        st.markdown('<hr>', True)
        st.write('Data with all positive polarities')
        pos_df = posts_df[posts_df['polarity'] > 0]
        pos_df.reset_index(inplace=True, drop = True)
        st.dataframe(pos_df)
        csvp = pos_df.to_csv().encode()
        b64 = base64.b64encode(csvp).decode()
        hrefp = f'<a href="data:file/csvp;base64,{b64}" download="Positive.csv" target="_blank">Download csv file</a>'
        st.markdown(hrefp, unsafe_allow_html=True)

        st.markdown('<hr>', True)
        st.write('Data with all Neutral polarities')
        new_df = posts_df[posts_df['polarity'] == 0]
        new_df.reset_index(inplace=True, drop = True)
        st.dataframe(new_df)
        csvnew = new_df.to_csv().encode()
        b64 = base64.b64encode(csvnew).decode()
        hrefnew = f'<a href="data:file/csvnew;base64,{b64}" download="Neutral.csv" target="_blank">Download csv file</a>'
        st.markdown(hrefnew, unsafe_allow_html=True)

        st.markdown('<hr>', True)
        st.write('Data with all Negative polarities')
        ne_df = posts_df[posts_df['polarity'] < 0]
        ne_df.reset_index(inplace=True, drop = True)
        st.dataframe(ne_df)
        ne_df = ne_df.to_csv().encode()
        b64 = base64.b64encode(ne_df).decode()
        hrefne = f'<a href="data:file/ne_df;base64,{b64}" download="Negative.csv" target="_blank">Download csv file</a>'
        st.markdown(hrefne, unsafe_allow_html=True)
    else:
        st.markdown('<hr>', True)
        st.info('Fill all details and press the "Get Data" button.')