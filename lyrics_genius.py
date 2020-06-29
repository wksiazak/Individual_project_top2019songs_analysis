import lyricsgenius
import pandas as pd
import xlrd
from textblob import TextBlob
genius = lyricsgenius.Genius("oXwjl5H6WB9lmUawimm4u_YqDI5Z3PHsC33GNtQZCJFdYoN7HmLgpO5WJR-OdryS")
#I used data from webscrapping, but saved *txt as xls, because removed some characters like "&amp"
top2019billboard = pd.read_excel('list_scrapped_songs.xlsx')#top2019billboard.drop('rank_no')
#top2019billboard.reset_index()
pd.set_option('display.max_columns', None)
#print(top2019billboard)

def get_lyrics(title, artist):
  try:
    return genius.search_song(title, artist).lyrics
  except:
    return 'not found'

#Use get_lyrics funcion to get lyrics for every song in dataset
lyrics = top2019billboard.apply(lambda row: get_lyrics(row['song'], row['artist']), axis =1)
top2019billboard['Lyrics'] = lyrics
top2019billboard = top2019billboard.drop(top2019billboard[top2019billboard['Lyrics'] == 'not found'].index) #drop rows where lyrics are not found on Genius
print (top2019billboard.shape)


text = " ".join(text_song for text_song in top2019billboard.Lyrics)
blob_billboard2019 = TextBlob(text)
# Print out its sentiment
print(blob_billboard2019 .sentiment)