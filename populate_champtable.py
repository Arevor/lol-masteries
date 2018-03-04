#this is a mess
#you need a file named api_key with the rito key in it
#run this to create sqlite3 db file & a table with champion(name, title, id)

import sqlite3
import requests
import json
#connect to db file, or create if empty
conn = sqlite3.connect('masteryi.db')
#get API_KEY and GET
with open('api_key', 'r') as infile:
    API_KEY = infile.readline().rstrip()
r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false' +'&api_key=' + API_KEY)
r = r.json()
#cache response in text file
with open('cached_response_timestamp', 'w') as outfile:
    json.dump(r, outfile)

#load up cached response, create table if not made
data = json.load(open('cached_response_timestamp'))
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS `CHAMPIONS` (`Name`	TEXT NOT NULL, `Title`	TEXT NOT NULL, `championID`	INTEGER NOT NULL UNIQUE )")
conn.commit()

#dump data
for k, v in data.items():
    for kk, vv in v.items():
        print (vv['id'])
        id = vv['id']
        name = vv['name']
        title = vv['title']
        try:
            c = conn.cursor()
            c.execute("INSERT INTO CHAMPIONS values (?, ?, ?)", (name, title, id))
            conn.commit()
        except sqlite3.IntegrityError:
            print("dupe")