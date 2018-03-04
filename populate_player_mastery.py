import sqlite3
import requests
import json
import argparse
# connect to db file, or create if empty
conn = sqlite3.connect('masteryi.db')
c = conn.cursor()

# get API_KEY  from file, and summoner ID from argv1
with open('api_key', 'r') as infile:
    API_KEY = infile.readline().rstrip()
parser = argparse.ArgumentParser()
parser.add_argument("summonerID")
args = parser.parse_args()

# make the request and cache it in a file
req_url = 'https://na1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/'
r = requests.get(req_url + args.summonerID +'?api_key=' + API_KEY)
r = r.json()
with open(('cached_mastery_'+ args.summonerID), 'w') as outfile:
    json.dump(r, outfile)

# if the table doesnt exist, create it.
SQL = "CREATE TABLE IF NOT EXISTS `PLAYERMASTERY` (`championLevel` INTEGER NOT NULL, `chestGranted`	TEXT NOT NULL, " \
      "`championPoints`	INTEGER NOT NULL, `championPointsSinceLastLevel`	INTEGER NOT NULL, `playerID`	" \
      "INTEGER NOT NULL, `championPointsUntilNextLevel`	INTEGER NOT NULL, `tokensEarned`	INTEGER NOT NULL, " \
      "`championID`	INTEGER NOT NULL, `lastPlayTime`	INTEGER NOT NULL UNIQUE )"
c.execute(SQL)
conn.commit()

# iterate over the response, and dump new values into table
# lastPlayTime is the unique key, this is my way of 'Upserting' as sqlite3 doesn't support it :(
data = json.load(open('cached_mastery_' + args.summonerID))
for row in data:
    row_data = (row['championLevel'], row['chestGranted'], row['championPoints'], row['championPointsSinceLastLevel']
                , row['playerId'], row['championPointsUntilNextLevel'], row['tokensEarned'], row['championId'],
                row['lastPlayTime'])
    try:
        c.execute("INSERT INTO PLAYERMASTERY values(?, ?, ?, ?, ?, ?, ?, ?, ?)", (row_data))
        print ('updated values for ', row['championId'])
    except sqlite3.IntegrityError:
        print (row['championId'], ' ignored, values already exist')
    conn.commit()