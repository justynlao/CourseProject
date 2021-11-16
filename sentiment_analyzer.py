from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import re

# Player name dictionary; keys for csv file names, values for querying
PLAYERS = {"steph": "Stephen Curry", "lebron": "Lebron James", "durant": "Kevin Durant"}
# Individual years to get data from
YEARS = [2018, 2019, 2020]


def read_file(file_name):
    with open(file_name, encoding="utf8") as f:
        return f.readlines()


def clean_data(data):
    # Remove all non-alpha-numeric characters; remove lines longer than 300 chars
    data = [re.sub('[^a-zA-Z0-9 ]+', '', line) for line in data if len(line) < 300]
    return data


def main():
    for key in PLAYERS:
        for year in YEARS:
            print(f'Analyzing {PLAYERS[key]} from {year}...')

            # Convert csv files to lists
            titles = read_file(f'./data/{key}_data/{key}_titles_{year}.csv')
            comments = read_file(f'./data/{key}_data/{key}_comments_{year}.csv')

            # Clean and merge data lists
            cleaned_titles = clean_data(titles)
            cleaned_comments = clean_data(comments)
            cleaned_titles.extend(cleaned_comments)

            # Get polarity scores for each line in dataset
            scores = []
            for line in cleaned_titles:
                sia = SentimentIntensityAnalyzer()
                pol_score = sia.polarity_scores(line)
                pol_score['line'] = line
                scores.append(pol_score)

            # Label data as positive/neutral/negative
            scores_df = pd.DataFrame.from_records(scores)
            scores_df['label'] = 0
            scores_df.loc[scores_df['compound'] > 0.2, 'label'] = 1
            scores_df.loc[scores_df['compound'] < -0.2, 'label'] = -1

            # Output labeled data to csv file
            labeled_df = scores_df[['line', 'label']]
            labeled_df.to_csv(f'./data/{key}_data/{key}_{year}_labeled.csv', header=False, index=False, encoding='utf-8', mode='a')

            # Create dataframe for counts of positive/neutral/negative labels
            label_count_df = pd.DataFrame()
            label_count_df['count'] = scores_df.label.value_counts()
            label_count_df['normalized count'] = scores_df.label.value_counts(normalize=True) * 100
            label_count_df.to_csv(f'./data/{key}_data/{key}_{year}_label_counts.csv', encoding='utf-8')


if __name__ == "__main__":
    main()
