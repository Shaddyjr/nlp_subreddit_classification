# This file gathers data from the Reddit API and saves the result as a CSV file

### Table of contents ###
# 1) Imports
# 2) Main Setup
# 3) Main

## IMPORTS ##
import pandas as pd
import requests
import time
import logging
import sys
import os

from math import floor

## MAIN SETUP ##
data_folder_name = "data"
save_file_name   = "subreddit_data.csv"
log_file_name    = "reddit_api.log"

# default subreddits
subreddit_0 = "deathnote"
subreddit_1 = "OnePunchMan"

# ensure data folder exists
if data_folder_name not in os.listdir():
    os.mkdir(data_folder_name)

# generalized for any two arbitrary subreddits by user
# Ex. `python gathering_data.py subreddit_0 subrreddit_1`
if 2 < len(sys.argv):
    subreddit_0 = sys.argv[1]
    subreddit_1 = sys.argv[2]

# Loggin setup 
logging.basicConfig(
    level    = logging.DEBUG, 
    filename = log_file_name, 
    filemode = 'a', 
    format   = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt  = '%m-%d-%Y %H:%M:%S'
)

def get_subreddit_posts(subreddit, n = 1300):
    '''
    Returns a list of the JSON data from the given subreddit.
    
    params:
        n (int) : the number of posts to request (default: 1300)
    '''
    URL = f"https://www.reddit.com/r/{subreddit}.json"
    headers = {"User-agent":f"Reddit-{subreddit} bot 0.1"}
    
    output = []
    iters  = round(n / 100)
    params = {"limit" : 100}
    
    logging.info(f"Starting {subreddit} API request:")
    for i in range(iters + 1):
        req  = requests.get(URL, params = params, headers = headers)
        json = req.json()
        output.extend(json["data"]["children"])
        params["after"] = json["data"]["after"] # using next chunk for next iteration
        
        # logging feedback
        perc = (i+1)/iters
        if floor(perc*10) % 3 == 0 :
            logging.info(f"{round(perc * 100, 2)}% done!")
        if perc == 1:
            break
        time.sleep(1)
    logging.info(f"Completed {subreddit} API request!")

    return output

def format_post_from_json(post, label):
    '''
    Returns formatted dictionary of subreddit with label.

    INPUT:
        post (dict): subreddit post
        label (int/string): subreddit relabel
    '''
    return {
        "subreddit" : label,
        "title"     : post["title"]
    }

def create_posts_from_json_list(json_list, label):
    return [format_post_from_json(row["data"], label) for row in json_list]

## MAIN ##
def main():
    # get data
    subreddit_0_data = create_posts_from_json_list(get_subreddit_posts(subreddit_0), label = 0)
    subreddit_1_data = create_posts_from_json_list(get_subreddit_posts(subreddit_1), label = 1)

    # create dataframe
    df = pd.DataFrame(subreddit_0_data + subreddit_1_data)
    # remove duplicates
    df.drop_duplicates(inplace = True) # keeps first duplicate by default
    # save to csv
    df.to_csv(f"{data_folder_name}/{save_file_name}", index = False)

# Only run when file is directly executed (not when imported)
if __name__ == '__main__':
    main()