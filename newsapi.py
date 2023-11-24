import requests
import datetime
import os
import json
import pandas as pd
from functools import reduce
import math
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

def selectSomeData(total, df):
    if total >= len(df):
        return df
    # randomly select data from each keyword in a proportional way
    # get all distinct keywords and its count
    df["keyword"] = df["keyword"].apply(", ".join) # convert list to string
    df_keyword = df["keyword"].value_counts()
    keyword_dict = df_keyword.to_dict() #key: keywords(name of movies), value: num of occurence
    total_data = len(df)
    # calculate the ratio
    first_key = ""
    for key in keyword_dict:
        if first_key == "":
            first_key = key
        occurence = keyword_dict[key]
        # out of <total_data>, <key> appears <occurence> times,
        # if total data is <total>, key will appear '(occurence * total) / total_data' times
        val = math.ceil((occurence * total) / total_data) 
        keyword_dict[key] = val  # overwrite with the new val
    
    # filter data to be only the first keyword
    # then randomly select data with amount = keyword_dict[first_key]
    random_data = df[df["keyword"] == first_key].sample(n=keyword_dict[first_key])
    for key in keyword_dict:
        if key == first_key:
            continue
        cur_data = df[df["keyword"] == key].sample(n=keyword_dict[key])
        random_data = pd.concat([random_data, cur_data], axis=0)  # merge <cur_data> into <random_data>
   
    # <random_data> does non contain exactly <total> rows bc use math.ceil
    random_data = random_data.sample(n=total)
    # convert keyword col back to list
    random_data["keyword"] = random_data["keyword"].apply((lambda x: x.split(", ")))
    return sortDfOnKeyword(random_data)

def combineKeywordCol(series):
    # return reduce(lambda x, y: [x] + [y] if type(x) is not list else x + [y], series)
    return reduce(lambda x, y: x + y, series)

def keywordColSort(arr):
    return (len(arr), arr)

def sortDfOnKeyword(df):
    df["sort_by_keyword"] = df["keyword"].apply(keywordColSort)
    df = df.sort_values(by="sort_by_keyword", ascending=False)
    return df.drop(columns=["sort_by_keyword"])

def addKeywordCol(files):
    # input is list of files
    # convert each files into dataframe and add new column with the name of file 
    all_data = []
    for i in range(len(files)):
        # get list of data of current file
        data = openFile(files[i])
        # for each data, add filename
        for d in data:
            index = files[i].rfind("/") # index of last occurence of "/"
            d['keyword'] = [files[i][index+1:]] # get only the file name
        # append to the main list
        all_data = all_data + data

    # convert all_data to dataframe
    df =  pd.DataFrame.from_dict(all_data)

    col = ["title", "description", "url", "publishedAt", "keyword"]
    filter_col = ["title", "description", "url", "publishedAt"]
    df = df[col]
    new_df = df.groupby(filter_col).agg(combineKeywordCol).reset_index()
   
    return sortDfOnKeyword(new_df)
    # new_df["sort_by_keyword"] = new_df["keyword"].apply(keywordColSort)
    # new_df = new_df.sort_values(by="sort_by_keyword", ascending=False)
    # return new_df.drop(columns=["sort_by_keyword"])

def combineMovieData(dataFolder, total, output_file1, output_file2):
    # combine files under movies folder into one
    # output_file1: for all data, output_file2: for <total> number of data

    # get all files under <dataFolder> folder
    files_arr = [f for f in os.listdir(dataFolder) if os.path.isfile(os.path.join(dataFolder, f))]
    for i in range(len(files_arr)):
        files_arr[i] = dataFolder + '/' + files_arr[i]
    
    df = addKeywordCol(files_arr)
    filter_df = selectSomeData(total, df.copy(deep=True))

    # create directory if not exist
    os.makedirs(os.path.dirname(output_file1), exist_ok=True)
    os.makedirs(os.path.dirname(output_file2), exist_ok=True)
    # save to file
    df.to_csv(output_file1, sep="\t", index=False)
    filter_df.to_csv(output_file2, sep="\t", index=False)


if __name__ == '__main__':
    lookback = 30
    output = 'movies'

    combineMovieData(output, 700, "results/res_all.tsv", "results/res_700.tsv")

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

