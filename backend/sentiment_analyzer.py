from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import re
from nba_api.stats.static import players
from pymongo import MongoClient
import os


# Establish mongodb connection
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')

client = MongoClient(f'mongodb+srv://{db_user}:{db_pass}@cluster0.yfg5a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.playerSentiments
players_collection = db.players

# List of names of all active players
ACTIVE_PLAYERS = [{'player_id': player['id'], 'full_name': player['full_name']} for player in players.get_active_players()]

# Individual years to get data from
YEARS = [2021]


def read_file(file_name):
    """ Opens file and returns list of lines. """
    with open(file_name, encoding="utf8") as f:
        return f.readlines()


def clean_data(data):
    """ Cleans text data; removes non-alpha-numeric characters and
    removes lines longer than 300 characters. """
    data = [re.sub('[^a-zA-Z0-9 ]+', '', line) for line in data if len(line) < 300]
    return data


def analyze_titles():
    """ Perform sentiment analysis on post titles. """
    for player in ACTIVE_PLAYERS:
        name_formatted = "_".join(player['full_name'].split())
        for year in YEARS:
            print(f'Analyzing {player["full_name"]} post titles from {year}...')

            # Read data from file
            try:
                titles = read_file(f'./data/2021_data/submission_titles/{name_formatted}_Titles.csv')
            except FileNotFoundError:
                player['title_polarity_counts'] = {'neutral': 0, 'positive': 0, 'negative': 0}
                query = {"full_name": player["full_name"]}
                players_collection.update_one(query, {"$set": player}, upsert=True)
                continue

            # Clean text data
            cleaned_titles = clean_data(titles)

            # Get polarity scores on each line of text data
            scores = []
            sia = SentimentIntensityAnalyzer()
            for title in cleaned_titles:
                pol_score = sia.polarity_scores(title)
                pol_score['title'] = title
                scores.append(pol_score)

            # Label scores based on a threshold
            scores_df = pd.DataFrame.from_records(scores)
            scores_df['label'] = 'neutral'
            scores_df.loc[scores_df['compound'] > 0.2, 'label'] = 'positive'
            scores_df.loc[scores_df['compound'] < -0.2, 'label'] = 'negative'
            player['title_polarity_counts'] = scores_df.label.value_counts(sort=False).to_dict()

            # Insert/Update documents in MongoDB database
            query = {"full_name": player["full_name"]}
            players_collection.update_one(query, {"$set": player}, upsert=True)


def analyze_comments():
    """ Perform sentiment analysis on comments. """
    for player in ACTIVE_PLAYERS:
        name_formatted = "_".join(player['full_name'].split())
        for year in YEARS:
            print(f'Analyzing {player["full_name"]} comments from {year}...')

            # Read data from file
            try:
                comments = read_file(f'./data/2021_data/comments/{name_formatted}_comments.csv')
            except FileNotFoundError:
                player['comment_polarity_counts'] = {'neutral': 0, 'positive': 0, 'negative': 0}
                query = {"full_name": player["full_name"]}
                players_collection.update_one(query, {"$set": player}, upsert=True)
                continue

            # Clean text data
            cleaned_comments = clean_data(comments)

            # Get polarity scores on each line of text data
            scores = []
            sia = SentimentIntensityAnalyzer()
            for comment in cleaned_comments:
                pol_score = sia.polarity_scores(comment)
                pol_score['comment'] = comment
                scores.append(pol_score)

            # Label scores based on a threshold
            scores_df = pd.DataFrame.from_records(scores)
            scores_df['label'] = 'neutral'
            scores_df.loc[scores_df['compound'] > 0.2, 'label'] = 'positive'
            scores_df.loc[scores_df['compound'] < -0.2, 'label'] = 'negative'
            player['comment_polarity_counts'] = scores_df.label.value_counts(sort=False).to_dict()

            # Insert/Update documents in MongoDB database
            query = {"full_name": player["full_name"]}
            players_collection.update_one(query, {"$set": player}, upsert=True)


if __name__ == "__main__":
    analyze_titles()
    analyze_comments()
