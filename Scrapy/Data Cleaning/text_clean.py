from googletrans import Translator
import json
import re

translator = Translator()

raw_content = open("../song_lyrics.json", 'r').read()

lyric_obj = json.loads(raw_content)

converted_fileds = ["artist", "music", "genre"]


def translate_sentence(text):
    response = translator.translate(text,dest='si')
    return response.text

def format_array(text):

    translated_result = translate_sentence(text).split(",")
    return translated_result

def format_title_sin(title_sin, title_en):
    if(title_sin==None):
        print(title_en)
        title_sin = translate_sentence(re.split('–|-|\|', title_en)[1])
        return title_sin
    else:
        return title_sin

def format_title_en(title_en):
    if(title_en!=None):
        formated_title = re.split(", |_|-|!|",title_en)[0].strip()
        return formated_title
    else:
        return title_en

for index in range(0,len(lyric_obj)):
    song = lyric_obj[index]

    artist_sin = format_array(song['artist'])
    music_sin = format_array(song['music'])
    genre_sin = format_array(song['genre'])
    writer_sin = format_array(song['writer'])
    rating_formated = int(song['rating'].replace(",",""))
    title_si_formated = format_title_sin(song['title_sin'], song['title_en'])
    title_en_formated = format_title_en(song['title_en'])

    lyric_obj[index]['artist'] = artist_sin
    lyric_obj[index]['music'] = music_sin
    lyric_obj[index]['genre'] = genre_sin
    lyric_obj[index]['writer'] = writer_sin
    lyric_obj[index]['rating'] = rating_formated

    lyric_obj[index]['title_en'] = title_en_formated
    lyric_obj[index]['title_sin'] = title_si_formated

    if(lyric_obj[index]['title_sin']==None):
        print(lyric_obj[index])
    #print(song)




dump_obj = json.dumps(lyric_obj)

wrt_file = open("clean_lyrics.json",'w')
wrt_file.write(dump_obj)
wrt_file.close()
