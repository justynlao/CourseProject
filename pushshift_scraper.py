import pandas as pd
from pmaw import PushshiftAPI
import datetime as dt

# Player name dictionary; keys for csv file names, values for querying
PLAYERS = {"steph": "Stephen Curry", "lebron": "Lebron James", "durant": "Kevin Durant"}
# Individual years to get data from
YEARS = [2018, 2019, 2020]


class RedditScraper:
    def __init__(self, subreddit, before, after, submission_limit=1000, comment_limit=100000):
        self.api = PushshiftAPI()
        self.subreddit = subreddit
        self.before = before
        self.after = after
        self.submission_limit = submission_limit
        self.comment_limit = comment_limit

    def get_submission_titles(self, queries, year):
        """ Retrieves submission titles on given queries. """
        for key, value in queries.items():
            print(f'Retrieving post titles on {value} from {year}...')
            submissions = self.api.search_submissions(title=value, subreddit=self.subreddit, limit=self.submission_limit,
                                                      before=self.before, after=self.after, filter="title", sort_type="score")
            titles_df = pd.DataFrame(submissions)['title']
            titles_df = titles_df.replace(r'\n', ' ', regex=True)
            titles_df.to_csv(f'./data/{key}_titles_{year}.csv', header=False, index=False, encoding='utf-8')

    def get_comments(self, queries, year):
        """ Retrieves comments on given queries. """
        for key, value in queries.items():
            print(f'Retrieving comments on {value} from {year}...')
            comments = self.api.search_comments(q=value, subreddit=self.subreddit, limit=self.comment_limit,
                                                before=self.before, after=self.after, filter="body")
            comments_df = pd.DataFrame(comments)['body']
            comments_df = comments_df.replace(r'\n', ' ', regex=True)
            comments_df.to_csv(f'./data/{key}_comments_{year}.csv', header=False, index=False, encoding='utf-8')

    def get_comments_by_id(self, queries, year):
        """ Retrieves comments in submissions on given queries. """
        for key, value in queries.items():
            print(f'Retrieving comments by id on {value} from {year}...')
            post_ids = self.get_submission_ids(value)
            comment_ids = self.get_comment_ids(post_ids)
            comments = self.api.search_comments(ids=comment_ids, filter="body")
            comments_df = pd.DataFrame(comments)
            comments_df = comments_df.replace(r'\n', ' ', regex=True)
            comments_df.to_csv(f'./data/{key}_comments_{year}.csv', header=False, index=False, encoding='utf-8')

    def get_submission_ids(self, query):
        """ Retrieves submission ids on a given query. """
        print(f'Retrieving post_ids...')
        submissions = self.api.search_submissions(title=query, subreddit=self.subreddit, limit=self.submission_limit,
                                                  before=self.before, after=self.after, filter="id")
        post_ids = [post['id'] for post in submissions]
        return post_ids

    def get_comment_ids(self, post_ids):
        """ Retrieves comment ids given submission ids. """
        print(f'Retrieving comment ids...')
        comments = self.api.search_submission_comment_ids(ids=post_ids)
        comment_ids = [c_id for c_id in comments]
        return comment_ids


def main():
    for year in YEARS:
        before = int(dt.datetime(year, 12, 1, 0, 0).timestamp())
        after = int(dt.datetime(year, 1, 1, 0, 0).timestamp())
        nba_scraper = RedditScraper("nba", before, after, 500, 10000)
        nba_scraper.get_submission_titles(PLAYERS, year)
        nba_scraper.get_comments(PLAYERS, year)


if __name__ == "__main__":
    main()
