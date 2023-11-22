import requests
import datetime
import os
import json
import pandas as pd
from functools import reduce

from datetime import date

API_KEY = "22c05da432d1401a922f84a455e251b7"
TODAY = date.today()
LANGUAGE = "en"

ARTICLES_QUERY_STRING_TEMPLATE = "https://newsapi.org/v2/everything?q={}&from={}&language={}&apiKey={}"

# queries NewsAPI and returns python list of english news articles 
#   (represented as dicts) containing news_keywords and published in the last <lookback> days
def fetch_latest_news(api_key, news_keywords, lookback=10):

    keywords = "+AND+".join(news_keywords)
    date_to_sub = datetime.timedelta(lookback)
    from_date = TODAY-date_to_sub
    query_string = ARTICLES_QUERY_STRING_TEMPLATE.format(keywords, from_date, LANGUAGE, api_key)

    response = requests.get(query_string)


    
    data = response.json()

    if data["status"] == "error":
         raise Exception("unable to fetch articles")

    return data["articles"]


def openFile(input_file):
    # open json file and return as dict
    with open(input_file) as json_file:
        data = json.load(json_file)
    return data

def combineFileNameCol(series):
    #return reduce(lambda x, y: [x] + [y] if type(x) is not list else x + [y], series)
    return reduce(lambda x, y: x + y, series)

def addFileNameCol(files):
    # input is list of files
    # convert each files into dataframe and add new column with the name of file 
    all_data = []
    for i in range(len(files)):
        # get list of data of current file
        data = openFile(files[i])
        # for each data, add filename
        for d in data:
            d['filename'] = [files[i][7:]] # [7:] -> remove the 'movies/' part
            d['occurence'] = 1
        # append to the main list
        all_data = all_data + data

    
    # convert all_data to dataframe
    df =  pd.DataFrame.from_dict(all_data)

    col = ["title", "description", "url", "publishedAt", "filename", "occurence"]
    filter_col = ["title", "description", "url", "publishedAt"]
    df = df[col]
    new_df = df.groupby(filter_col).agg(combineFileNameCol).sort_values(by="occurence", ascending=False)
    return new_df

def combineMovieData():
    # combine files under movies folder into one
    # get all files under movies(output) folder
    files_arr = [f for f in os.listdir(output) if os.path.isfile(os.path.join(output, f))]
    
    for i in range(len(files_arr)):
        files_arr[i] = output + '/' + files_arr[i]
    
    df = addFileNameCol(files_arr)
    #df.to_csv('res.tsv', sep="\t")


if __name__ == '__main__':
    lookback = 30
    output = 'movies'





    # with open(os.path.join(output, "hunger_games"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["The Ballad of Songbirds and Snakes"], lookback), f, indent=4)
    # with open(os.path.join(output, "the_marvels"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["The Marvels"], lookback), f, indent=4)
    # with open(os.path.join(output, "anatomy_of_a_fall"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["Anatomy of a Fall"], lookback), f, indent=4)    
    # with open(os.path.join(output, "barbie_movie"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["Barbie"], lookback), f, indent=4)
    # with open(os.path.join(output, "oppenheimer"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["Oppenheimer"], lookback), f, indent=4)
    # with open(os.path.join(output, "astroid_city"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["Astroid City"], lookback), f, indent=4)
    # with open(os.path.join(output, "transformers"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["Transformers Rise of the Beasts"], lookback), f, indent=4)
    # with open(os.path.join(output, "saltburn"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["Saltburn"], lookback), f, indent=4)
    # with open(os.path.join(output, "trolls"), 'w') as f:
    #     json.dump(fetch_latest_news(API_KEY, ["Trolls Band Together"], lookback), f, indent=4)

