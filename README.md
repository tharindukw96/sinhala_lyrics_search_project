# Sinhala Song Lyrics Search Engine

- A text based sinhala song lyrics search engine implemented using ElasticSearch
- The project is developed as a IR project CS4642 Data Mining and Information Retrieval under the supervision of Dr.U.Thayasivam at University of Moratuwa.

## Introduction

### What is ElasticSearch ?

Elasticsearch is a RESTful powerful indexing and search tool, which is a part of the Elastic Stack.
Elasticsearch is horizontally scalable, which is ideal for music data, whose size may go up to a few GBs.
Elasticsearch is also highly available, has flexible data model, and boasts rapid query execution.
Since the goal is to develop a Music Search Engine, Elasticsearch qualfies as a fast and reliable searching tool.

### Setting up ElasticSearch

On this project Elasticsearch is run on the localhost. Elasticsearch can be download from the official web site https://www.elastic.co/downloads/elasticsearch.
Extract the downloaded zip file and browse into "elasticsearch-x.x.0/bin" folder. Run ./elasticsearch on terminal. The default port for Elasticsearch web interface is 9200 or you can change it by changing http.port inside the elasticsearch.yml file present in bin directory. You can check if the server is up and running by browsing http://localhost:9200. It will return a JSON object, which contains the information about the installed Elasticsearch in the following manner.

```
{
  "name" : "tharindu-Inspiron-13-7378",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "-Pzel_6yRKiOZTrYJaxQoA",
  "version" : {
    "number" : "7.7.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "ad56dce891c901a492bb1ee393f12dfff473a423",
    "build_date" : "2020-05-28T16:30:01.040088Z",
    "build_snapshot" : false,
    "lucene_version" : "8.5.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

```
### Data

The lyrics data contains in the song_lyrics.json file. It has 1096 song lyrics with seven metadata(attributes). The meta data are Sinhala title, Artist name, Music composer name, Writer name, Rating, Genre, Singlish title. All the song lyrics and metadata are in the Sinhala language. The dataset is created by scraping the Sinhala lyrics web pages. 

1. Scraping
  - The scraping of the web pages is done by using the Scrapy python library. The Scrapy folder contains the all the details of the web scraping. The web scraping spider code can be found in lyric_spider.py. The output of the script is written to the song_lyrics.json file.

2. Data Cleaning & Preprocessing
  - Several prepocessing has done to the song_lyrics.json file. The lyric data is mixed with the guitar chords. The chords have to remove from the lyrics. Also writter name, artist name, genre, music composer names are in sinhala on the website. The names are translated to Sinhala using google translator (text_clean.py). Several names can't be converted to Sinhala, So further preprocessing and name translation is done(IR_project_Fix_missing_Sinhala_names.ipynb). The final cleaned version of dataset is in the clean_song_lyrics.json.
  
### Creating Indices on ElasticSearch

Kibana is used in this project for easily explore the Elasticsearch services. The all ElasticSearch data is in the ES folder.Before add the data to the ES, first the index shoud be defined. Kibana is really useful to add data, create index and retrive data.I have create a index named "sinhala_songs". The complete index creation json object can be found in the mapping.json.

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
### Indexing and Querying Techniques Used

1. Tokenizer
  - ICU_tokenizer 
    - This tokenizer is best for the text from unicode languages. ICU tokenizer is used for document tokenizing(indexing time).
  - Standard Tokenizer 
    - Standard tokenizer is used during the query tokenizing.
  
2. Stop word filtering

3. Character filters 
  - Custom character filter is used. The special characters (‘ “ , | \ / ) are replaced with space in query time and removed in document     indexing. 

4. N Edge Gram Filter 
  - N edge gram filter used for query and document indexing(all fields except lyrics). This filter generates n-grams for each token. Used to identify spelling mistakes.

### Advanced Features
1. Facet and Range queries
  - The search engine support for range queries such as top songs, top songs of Amaradewa, Top songs written by Yamuna Malani, etc. Also, facet queries are supported such as the number of songs for each genre for the search results.
  
2. Rule-base classification 
  - The query was going through a query pre-processing task before the request from ElasticSearch. This was done on the python backend. The query is tokenized by Sinling Sinhala tokenizer and check the affix and base with a specific set of words. This can identify the context of the query(asked for an artist, ask for a writer, ask for best songs, etc).
  
3. Boosting queries
  - The system is boosting queries by Elasticsearch boost. The individual fields set with higher weights after identifying the contexts such as artists, music composers, writers.

After create the "sinhala_songs" index , The next step is adding the document to the Elasticsearch. I have write a small script to insert the data into ElasticSearch(bulk_insert.py). This script take the csv file of the data collection and send documents to ES. The csv version of data set can be found in clean_song_lyrics.csv . Elasticsearch and Pandas additional python libraries are needed to run the bulk_insert.py. 

### Frontend & Backend

1. Frontend

  - The front end is a simple single page web application. It is implemented using HTML,Jquery andMatrialize CSS. The front is serve by the backend flask appication.

2. Backend

  - The backend is implemeted using the Python Flask framework. The additional python libraries can be found in requirement.txt.
  - Elasticsearch python library used to retirve the data from the ElasticSearch endpoint. 
    - To run the backend use following commans
      ```
      python index.py
      
      ```
    - The flask run the backend on the 127.0.0.1. You can browse 127.0.0.1:5000 for check the front end of the search engine.


