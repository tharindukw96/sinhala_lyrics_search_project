import scrapy
#import requests
from scrapy.spiders import SitemapSpider
from scrapy.http.request import Request
import re
import os
import json


class SongBookSpider(scrapy.Spider):
    name = "Lyric"
    allowed_domains = ["sinhalasongbook.com"]
    start_urls   = ["https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=" + str(page) for page in range(1, 23)]
    page = 0
    lyric_list = []

    def parse_song(self, response):
        separator = ','
        song_html = response

        title_en = (song_html.xpath('//div[@class="entry-content"]/h2/text()')).get()
        title_en = title_en.strip()

        title_sin = (song_html.xpath('//span[@class="sinTitle"]/text()')).get()

        artist_arr = song_html.xpath('//div[@class="su-row"]//span[@class="entry-categories"]//a/text()').extract()
        artist = (separator.join(artist_arr))

        genre_arr = song_html.xpath('//div[@class="su-row"]//span[@class="entry-tags"]//a/text()').extract()
        genre = (",".join(genre_arr))
        
        writer_arr = song_html.xpath('//div[@class="su-row"]//span[@class="lyrics"]//a/text()').extract()
        writer = (",".join(writer_arr))
        
        music_arr  = song_html.xpath('//div[@class="su-row"]//span[@class="music"]//a/text()').extract()
        music = (",".join(music_arr))

        rating_arr = song_html.xpath('//div[@class="tptn_counter"]/text()').extract()
        rating = "0"
        if(len(rating_arr)!=0):
            rating = "".join(rating_arr[0]).replace("-","").replace("Visits","").strip()

        print(title_en, title_sin, artist, genre, writer, music, rating)

        lyric_body = (song_html.xpath('//div[@class="entry-content"]//pre/text()').extract())
        lyric_body_arr = []
        for chunk in lyric_body:
            lines = chunk.split('\n')
            for line in lines:
                lyric_body_arr.append(line)
        
        clear_lyrics = ""
        chords = ""
        
        for line in lyric_body_arr:
            if(re.search('[a-zA-Z]', line)):
               chords = chords + line +"\n"
            else:
                if(len(line)!=0):
                    line = line.replace('+','')
                    line = line.replace('|','')
                    line.strip()
                    clear_lyrics = clear_lyrics + line + os.linesep
                
        self.lyric_list.append({
            'title_en': title_en,
            'title_sin': title_sin,
            'artist' : artist,
            'genre' : genre,
            'rating': rating,
            'writer' : writer,
            'music' : music,
            'song' : clear_lyrics
            })

        dump_song = json.dumps({
            'title_en': title_en,
            'title_sin': title_sin,
            'artist' : artist,
            'genre' : genre,
            'rating': rating,
            'writer' : writer,
            'music' : music,
            'song' : clear_lyrics
            })

        file  = open("song_lyrics.json", "a")
        file.write(","+dump_song)
        file.close()
        yield {
            'title_en': title_en,
            'title_sin': title_sin,
            'artist' : artist,
            'genre' : genre,
            'rating': rating,
            'writer' : writer,
            'music' : music,
            'song' : clear_lyrics
        }
        

    def parse(self, response):
        song_page_links = response.xpath('//div[@class="col-md-6 col-sm-6 col-xs-12 pt-cv-content-item pt-cv-1-col"]//a/@href').extract()
        for song_link in song_page_links:
            self.page = self.page + 1
            yield scrapy.Request(
                song_link,
                callback=self.parse_song
            )

        
        
        print("-----------------------count--------", self.page)