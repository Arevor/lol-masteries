#this is a mess
#you need a file named api_key with the rito key in it
#run this to create sqlite3 db file & a table with champion(name, title, id)

import sqlite3
import requests
import json
#connect to db file, or create if empty
conn = sqlite3.connect('masteryi.db')
#get API_KEY
with open('api_key', 'r') as infile:
    API_KEY = infile.readline().rstrip()

#make request and cache response
req_url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key='
r = requests.get(req_url + API_KEY)
r = r.json()
#cache response in text file
with open('cached_response_timestamp', 'w') as outfile:
    json.dump(r, outfile)

#load up cached response, create table if not made
data = json.load(open('cached_response_timestamp'))
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS `CHAMPIONS` (`Name`	TEXT NOT NULL, `Title`	TEXT NOT NULL, "
          "`championID`	INTEGER NOT NULL UNIQUE )")
conn.commit()

#dump data
for k, v in data.items():
    #values are within the "data" JSON tag
    for k2, v2 in v.items():
        id = v2['id']
        name = v2['name']
        title = v2['title']
        try:
            c = conn.cursor()
            c.execute("INSERT INTO CHAMPIONS values (?, ?, ?)", (name, title, id))
            conn.commit()
        #If champion already exists, do nothing
        except sqlite3.IntegrityError:
            print("")
conn.close()

