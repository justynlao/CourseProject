# NBA Subreddit Player Sentiment Analysis
This application compiles data from the r/nba subreddit and performs sentiment analysis on posts/comments for all active players for the 2021 NBA season. The web application displays the results along with doughnut charts to visualize the data.

## Table of Contents
1. [Introduction](#introduction)
2. [Code Overview](#codeoverview)
    1. [Data Retrieval](#dataretrieval)
    2. [Sentiment Analysis](#sentimentanalysis)
    3. [Creating a Flask API](#api)
    4. [Making a Web App](#webapp)
3. [Using the Application](#usingtheapplication)
4. [Built With](#builtwith)

## Introduction <a name="introduction"></a>
The NBA has hundreds of players, along with millions of fans that have their own favorite players, as well as their own hated players. The NBA Subreddit provides insight on which players might be liked and which players might be disliked by the general community, as the subreddit has upwards of 4 million subscribers.

Through this project, my goal was to determine which players are the most liked/disliked in the NBA Subreddit community, by analyzing post titles and comments about individual players. After retrieving data and performing sentiment analysis, I created a web application that compiles and visualizes the results.

## Code Overview and Implementation Details <a name="codeoverview"></a>
There are 4 main components to the code. First, I retrieved and cleaned the necessary data, then I performed sentiment analysis on the data, then I created an API to expose the data, and lastly I created a frontend to display the results.

### Data Retrieval <a name="dataretrieval"></a>
For retrieving the data, I started with the Python Reddit API Wrapper (PRAW). However, I quickly discovered that not only was PRAW limited in terms of quantity of data that could be retrieved, but it was also extremely slow. Thus, I looked into additional options and found PushShift, which is an API that allows for searching reddit data with powerful aggregations. In tandem with PushShift Multithread API Wrapper (PMAW), the data retrieval process became a lot more dynamic and fast. The code for this is detailed below.

Retrieving high quality data proved to be difficult for a couple of reasons. First, some players shared first or last names. Second, posts and comments often either did not explicitly mention player names at all or mentioned multiple names. I decided to compromise by querying based on full names of players, which unfortunately is not the best representation of the entire community, especially on a social media platform like Reddit.

#### /backend/pushshift_scraper.py
This file retrieves reddit data through the PushShift Reddit API and stores the data in csv files. I decided to limit the time range to 2021 data only, as there would have been far too much data if I included more years. I also decided to only retrieve data on active players as of the current NBA season. In addition, I set limits of up to 1000 post titles and 5000 comments per player (500+ players).
These are the two main functions used to retrieve the desired data.
```python
get_submission_titles()
get_comments()
```
The main process of both the functions is as follows: For each query (player names) perform the search. If any data was found, store it in a pandas dataframe, strip new line characters, and convert the dataframe to csv format. Additionally, I defined the program as a class, so with simple parameter changes, one could use this to retrieve data from different time periods or different subreddits.

### Sentiment Analysis <a name="sentimentanalysis"></a>
For performing sentiment analysis, I started by cleaning the data. A lot of the posts and comments contained irrelevant text such as links. Using regular expressions I filtered out non-alpha-numeric characters. 

#### /backend/sentiment_analyzer.py
This file performs sentiment analysis on the retrieved data using the NLTK library. The results were stored in a MongoDB database for later consumption by the frontend.
These are the two functions to analyze the post titles and comments. The functions utilize NLTK's pre-trained Vader model and provide polarity scores (positive, neutral, negative).
```python
analyze_titles()
analyze_comments()
```
The main process of both the functions is as follows: For each csv file, first clean irrelevant characters from the data. Next, initialize the NLTK Sentiment Analyzer, and store the polarity scores in an array. Then, convert the scores array into a pandas dataframe in order to easily label the data. I decided to use a threshold of [-0.2, 0.2] to determine labels. Compound scores above 0.2 were labeled positive and scores below 0.2 were labeled negative. Scores in between the thresholds were considered neutral. Lastly, counts of each label were determined and stored in a database.

### Creating a Flask API <a name="api"></a>
In order to then provide this data to a frontend, I created a simple Flask REST API. The API contains two endpoints for getting data.

#### /backend/api/app.py
The file initializes two routes.
```
/players
/players/<int:player_id>
```
The first route returns every player document from the database.
The second route queries the database based on a specified player_id to return a single player document.

### Making a Web App <a name="webapp"></a>
The final step of the project was building a frontend to display the data in a more user-friendly manner. I decided to use React.js/Next.js to make the application, as Next.js provides static generation as well as built-in page routing. This made it easy to create dynamic routes for each individual player page.

In terms of the application itself, there are a few key features. Every player is displayed on a "card", along with a decimal number. For the number, I decided to establish a positivity index calculated by (number of positives / number of negatives). I decided on this with YouTube's like/dislike ratio in mind. Based on the results, I then decided on thresholds of 3.0 and 2.0. Greater than 3.0 is positive, greater than 2.0 is neutral, and below that is negative. Each player "card" then routes to an individual player page, which most notably features a Doughnut chart visualizing the counts of each label (positive, neutral, negative). 

## Using the Application <a name="usingtheapplication"></a>

## Built With <a name="builtwith"></a>
#### Backend
Library/Package | Version
--------------- | -------
|PMAW | 2.1.0 |
|Pandas | 1.3.2 |
|NLTK | 3.6.5 |
|PyMongo | 4.0 |
|Flask | 2.0.2 |

#### Frontend
Library/Package | Version
--------------- | -------
|React.js | 17.0.2 |
|Next.js | 12.0.7 |
|Axios | 0.24.0 |
|Chart.js | 3.6.2 |
|MUI | 5.2.3 |
|MUI Icons | 5.2.1 |






