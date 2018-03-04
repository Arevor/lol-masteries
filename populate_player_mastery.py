import sqlite3
import requests
import json
#connect to db file, or create if empty
conn = sqlite3.connect('masteryi.db')
#get API_KEY and GET
with open('api_key', 'r') as infile:
    API_KEY = infile.readline().rstrip()

SUMMONER_ID = 'ayy lmao'

r = requests.get('https://na1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/'+ SUMMONER_ID +'?api_key=' + API_KEY)
r = r.json()
#cache response in text file
with open(('cached_mastery_'+ SUMMONER_ID), 'w') as outfile:
    json.dump(r, outfile)

#load up cached response, create table if not made
data = json.load(open('cached_mastery'))
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS `masteries` (`Name`	TEXT NOT NULL, `Title`	TEXT NOT NULL, `championID`	INTEGER NOT NULL UNIQUE )")
conn.commit()

