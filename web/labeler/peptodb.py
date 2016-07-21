import sqlite3 as lite
import json

# connects to the database
con = lite.connect('pepto.db')

# opens the json file
tweet_file = 'tweets_RUN_1.json'
tweet_info = []
info = []

# looks at the json data line by line
with open(tweet_file, 'r')    as f:
    # for each line, puts the value in a list for later insert into table
    for line in f:
        try:
            tweet = json.loads(line)
            info.append(tweet['id'])
            info.append(1)
            info.append(tweet['text'])
            info.append(line)
            tweet_info.append(info)
            info = []
        except ValueError:
            pass

with con:
    # creates a tweets table and inserts the values
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS tweets')
    cur.execute('CREATE TABLE tweets(tweetid BIGINT, runid BIGINT, status TEXT, statusvec TSVECTOR, tweet JSON)')
    for info in tweet_info:
        cur.executemany('INSERT INTO tweets(tweetid, runid, status, tweet) VALUES (?, ?, ?, ?)', (info,))

    # creates a count table
    cur.execute('DROP TABLE IF EXISTS count')
    cur.execute('CREATE TABLE count(tweetid BIGINT, count BIGINT)')

    # creates classification table
    cur.execute('DROP TABLE IF EXISTS classification')
    cur.execute('CREATE TABLE classification(tweetid BIGINT, runid TEXT, label_data TEXT, class TEXT, conf FLOAT)')

    # creates runs table
    cur.execute('DROP TABLE IF EXISTS runs')
    cur.execute('CREATE TABLE runs(runid TEXT, run_date TEXT, filter_text TEXT, userid TEXT)')
