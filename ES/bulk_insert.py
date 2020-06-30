#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import Python's JSON library for its loads() method
import json
import numpy as np
# import time for its sleep method
from time import sleep

# import the datetime libraries datetime.now() method
from datetime import datetime

# use the Elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers

# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("localhost:9200")


# define a function that will load a text file


def get_data_from_text_file(self):
    # the function will return a list of docs
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]

import pandas as pd
# call the function to get the string data containing docs
songs = pd.read_csv("song_lyrics(1).csv")
songs.drop(columns=['id'], inplace=True)
count = 0
# print the length of the documents in the string

# define an empty list for the Elasticsearch docs
doc_list = []

def row_to_json(row):
    global count
    count+=1
    return {
        "_id": count,
        "title_si" : row[2],
        "titile_singlsh": row[8], 	
        "rating": row[1], 	
        "genre": row[4],	
        "music": row[5],
        "writer": row[7],
        "lyrics": row[6].strip(),
        "artist": row[3], 
    }

print(songs.values[0])

# use Python's enumerate() function to iterate over list of doc strings
for doc in songs.values:
	try:
		# convert the string to a dict object
		dict_doc = row_to_json(doc)

		# append the dict object to the list []
		doc_list += [dict_doc]
	except Exception as err:
		# print the errors
		print ("ERROR for num:", err)
    

print ("Dict docs length:", len(doc_list))

# attempt to index the dictionary entries using the helpers.bulk() method
try:
    print ("\nAttempting to index the list of docs using helpers.bulk()")

    # use the helpers library's Bulk API to index list of Elasticsearch docs
    resp = helpers.bulk(
        client,
        doc_list,
        index="sinhala_songs",
        doc_type="_doc"
    )

    # print the response returned by Elasticsearch
    print ("helpers.bulk() RESPONSE:", resp)
    print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

except Exception as err:

    # print any errors returned w
    # Prerequisiteshile making the helpers.bulk() API call
    print("Elasticsearch helpers.bulk() ERROR:", err)
    quit()

# get all of docs for the index
# Result window is too large, from + size must be less than or equal to: [10000]
query_all = {
    'size': 10_000,
    'query': {
        'match_all': {}
    }
}

print ("\nSleeping for a few seconds to wait for indexing request to finish.")
sleep(2)

# pass the query_all dict to search() method
resp = client.search(
    index="sinhala_songs",
    body=query_all
)

print ("search() response:", json.dumps(resp, indent=4))

# print the number of docs in index
print ("Length of docs returned by search():", len(resp['hits']['hits']))

"""
Length of docs returned by search(): 5
"""
