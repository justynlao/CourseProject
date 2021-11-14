""" Program that scrapes and prints reddit submission info given a subreddit and queries.
"""


import praw
import json


# Player names to use as search queries
PLAYERS = ["Stephen Curry", "Lebron James"]


class RedditScraper:
    VALID_SORTS = ['relevance', 'hot', 'top', 'new', 'comments']
    VALID_TIMES = ['all', 'day', 'hour', 'month', 'week', 'year']

    def __init__(self, sub_name):
        """ Constructor; initializes PRAW reddit/subreddit instances and submissions dictionary. """
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(sub_name)
        self.submissions = {}

    def get_submissions(self, queries, sort="relevance", time_filter="year", limit=None):
        """ Get up to 1000 subreddit submissions that satisfy a given search query and filters. """
        if not isinstance(queries, list):
            print('Please enter a list of queries.')
            return

        if sort not in self.VALID_SORTS:
            print('Please enter a valid sort filter.')
            return

        if time_filter not in self.VALID_TIMES:
            print('Please enter a valid time filter.')
            return

        for query in queries:
            print(f'Retrieving posts about {query}...')

            query_submissions = []
            for submission in self.subreddit.search(query, sort=sort, time_filter=time_filter, limit=limit):
                query_submissions.append(submission)

            self.submissions[query] = query_submissions


def extract_submission_data(scraper):
    """ Given a RedditScraper object, extract key attributes from the submissions. """
    if not scraper.submissions:
        return

    print('Extracting submission data...')
    result = {}
    for query, submissions in scraper.submissions.items():
        data_list = []
        for sub in submissions:
            data = {"title": sub.title, "num_comments": sub.num_comments,
                    "score": sub.score, "upvote_ratio": sub.upvote_ratio, "url": sub.url}
            data_list.append(data)
        result[query] = data_list

    return json.dumps(result)


def main():
    NBAScraper = RedditScraper("nba")
    NBAScraper.get_submissions(PLAYERS)
    data = extract_submission_data(NBAScraper)
    print(data)


if __name__ == "__main__":
    main()
