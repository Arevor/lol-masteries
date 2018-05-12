* this script grabs all the mastery data for a player and dumps it into the DB. 
* you need a file named api_key with the rito key in it

# populate_champtable.py
* creates db schema with championName, title, and ID,
* used to grab champion name & title given an ID. 

# populate_player_mastery.py
* run via command line with summoner name as argument 
```BASH 
$ python3 populate_player_mastery.py Dyrus
```
* will create PlayerMastery table if not present, and dump all of the players mastery data into the table
