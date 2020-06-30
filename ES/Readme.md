# Elastic Search

Fore more information on setting up the ElasticSearch is on the home page of this repository. The final version of song lyrics and metadata are stores in the 
clean_song_lyrics.csv file. You can add data to ElasticSearch through Kibana. But I used a python script(bulk_insert.py) to add data to elastic search.

- First create a index named "sinhala_songs"

```
PUT sinhala_songs
{
    "settings": {
       "index": {
             "number_of_shards": 1,
             "number_of_replicas": 1
       },
       "analysis": {
         "analyzer": {
           "english_analyzer": {
               "type": "custom",
               "tokenizer": "lowercase",
               "char_filter":["punctuation_char_filter"],
               "filter": ["edge_n_gram_filter"]
           },
           "sinhala_analyzer_1": {
               "type": "custom",
               "tokenizer": "icu_tokenizer",
               "char_filter": ["punctuation_char_remove_filter"],
               "filter": ["edge_n_gram_filter"]      
           },
           "sinhala_analyzer_2": {
               "type": "custom",
               "tokenizer": "icu_tokenizer",
               "char_filter":["punctuation_char_filter"]    
           },
           "english_search_analyzer" : {
               "type": "custom",
               "tokenizer": "lowercase",
               "char_filter":["punctuation_char_filter"]
           },
           "sinhala_search_analyzer" : {
               "type": "custom",
               "tokenizer": "standard",
               "char_filter":["punctuation_char_remove_filter"]
           }
         },
         "char_filter": {
            "punctuation_char_filter":{
               "type":"mapping",
               "mappings":[".=>","|=>","-=>","_=>","'=>","/=>",",=>"]
            },
            "punctuation_char_remove_filter":{
               "type":"mapping",
               "mappings":[".=>\\u0020","|=>\\u0020","-=>\\u0020","_=>\\u0020","'=>\\u0020","/=>\\u0020",",=>\\u0020"]
            }
         },
         "filter": {
               "edge_n_gram_filter": {
                    "type" : "edge_ngram",
                    "min_gram":"2",
                    "max_gram":"20",
                    "side":"front"
               }
         }
       }
      }, 
      "mappings": {
           "properties": {
             "id": {
                  "type": "integer"
             },
             "titile_singlsh": {
                  "type": "text",
                  "analyzer":"english_analyzer",
                  "search_analyzer": "english_search_analyzer"
             },
             "title_si": {
                  "type": "text",  
                  "analyzer": "sinhala_analyzer_1",
                  "search_analyzer":"sinhala_search_analyzer"
             },
             "artist": {
               "type": "text",
                  "fields": {
                       "keyword":{
                          "type":"keyword"
                       }
                   },
                  "analyzer":"sinhala_analyzer_1",
                  "search_analyzer": "sinhala_search_analyzer"
             },
             "writer": {
               "type": "text",
                  "fields": {
                       "keyword":{
                          "type":"keyword"
                       }
                   },
                  "analyzer": "sinhala_analyzer_1",
                  "search_analyzer": "sinhala_search_analyzer"
             },
             "music": {
               "type": "text",
                  "fields": {
                       "keyword":{
                          "type":"keyword"
                       }
                   },
                  "analyzer": "sinhala_analyzer_1",
                  "search_analyzer": "sinhala_search_analyzer"
             },
             "genre": {
               "type": "text",
                  "fields": {
                       "keyword":{
                          "type":"keyword"
                       }
                   },
                  "analyzer": "sinhala_analyzer_1",
                  "search_analyzer": "sinhala_search_analyzer",
                  "fielddata": true
             },
             "rating": {
                  "type": "integer"
             },
             "lyrics": {
                  "type":"text",
                  "analyzer":"sinhala_analyzer_2",
                  "search_analyzer": "sinhala_search_analyzer"
             }
         }
       } 
}

```
If above command is succeeded , you will get the below response from elastic search. The above index configuration is in the [mapping.json](https://github.com/tharindukw96/sinhala_lyrics_search_project/blob/master/ES/mapping.json) file.

```
{"acknowledged": true}
```

- Then run the bulk_insert.py script to add all documents to elasticsearch. There are 1096 documents in the clean_song_lyrics.csv file.

- You can check the index information from kibana.
  > http://localhost:5601/app/kibana#/management/elasticsearch/index_management/indices
