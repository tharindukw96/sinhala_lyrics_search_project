
# Scraping

Scrapy is a free and open-source web-crawling framework written in Python. I use scrapy for web scraping task of this project. 

## Getting start with Scrapy
- Create a virtual environment.
```
$ python3.6 -m venv venv
$ source venv/bin/activate
```
- Install Scrapy.
```
 $ pip install scrapy
```
- Create a new Scrapy project.
```
$ scrapy startproject lyrics_scraping
```
- You will get follwing folder sctructure.
```
  - lyrics_scraping
      + __pycahce__
      + spiders
        init.py
        items.py
        middleware.py
        pipeline.py
        settings.py
```
- Copy the lyrics_spider.py into spiders folder.
- To start scraping.
```
$ scrapy crawl lyrics
```

## Data Cleaning
The scraped data is written into song_lyrics.json file. The data has to pre-process before index it. "Artist", "Music", "Genre", "Writer" fields are in the English language. The text_clean.py is translated in those fields from Engish to Sinhala. Requirements.txt contains the additional python libraries to install. 

> The googletrans library doesn't translate English names to Sinhala sometimes. So several names will still in English. Also, some names will translate with wrong Sinhala translation(This happens because the translator tries to translate some parts of the name as a word). 

- To fix the above issue, IR_project_Fix_missing_Sinhala_names.ipynb is used to replace the missing names with correct Sinhala representation.

