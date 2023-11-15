import requests
import datetime
import os
import json

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

if __name__ == '__main__':
    lookback = 30
    output = 'movies'

    with open(os.path.join(output, "hunger_games"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["The Ballad of Songbirds and Snakes"], lookback), f, indent=4)
    with open(os.path.join(output, "the_marvels"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["The Marvels"], lookback), f, indent=4)
    with open(os.path.join(output, "anatomy_of_a_fall"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["Anatomy of a Fall"], lookback), f, indent=4)    
    with open(os.path.join(output, "barbie_movie"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["Barbie"], lookback), f, indent=4)
    with open(os.path.join(output, "oppenheimer"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["Oppenheimer"], lookback), f, indent=4)
    with open(os.path.join(output, "astroid_city"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["Astroid City"], lookback), f, indent=4)
    with open(os.path.join(output, "transformers"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["Transformers Rise of the Beasts"], lookback), f, indent=4)
    with open(os.path.join(output, "saltburn"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["Saltburn"], lookback), f, indent=4)
    with open(os.path.join(output, "trolls"), 'w') as f:
        json.dump(fetch_latest_news(API_KEY, ["Trolls Band Together"], lookback), f, indent=4)