import pandas as pd
import pymysql
import sqlalchemy

#top50.csv includes only data for 2019 - top songs in 2019, we will compare topp100 songs for 2019 in Billboard with top spotify songs in 2019
spotify_data = pd.read_csv('top50.csv', encoding= 'ISO-8859-1', index_col=0)

class Spotify:

    def __init__(self):
        user = "TOPsongs_project_user"
        password = "qwerty1234"
        self.conn = pymysql.connect("localhost", user, password, "TOPsongs_project")
        self.c =self.conn.cursor()

    def createtabletop100songs(self):
        self.c.execute("create table spotify2019top("
                         "id_number int primary key auto_increment,"
                        "year int,"
                        "title varchar(255),"
                        "artist varchar(255))")
        self.conn.commit()

    def writeToSQLtable (self, dataframe, database, tablename):
        engine = sqlalchemy.create_engine('mysql+pymysql://TOPsongs_project_user:qwerty1234@localhost/TOPsongs_project')
        dataframe.to_sql(tablename, engine, if_exists='replace', index=False)

    def checkCommonSpotifyAndBillboard (self):
        self.c.execute("SELECT spotify2019top.Track, spotify2019top.Artist, top100songs.rank_no FROM spotify2019top LEFT JOIN top100songs ON spotify2019top.Track=top100songs.song_title WHERE top100songs.song_title is not NULL")
        common_songs = self.c.fetchall()
        print("_" * 70)
        print("List of  TOP songs which are common for Billboard and Spotify:")
        print("_"*70)
        print ("%30s|%30s|%3s|" % ("song", "artist", "billboard_2019_rank_no"))
        print("_" * 70)
        for common_song in common_songs:
            print("%30s|%30s|%3s|" % (common_song[0], common_song[1], common_song[2]))
        self.c.execute("SELECT COUNT( * ) FROM (SELECT spotify2019top.Track, spotify2019top.Artist, top100songs.song_title, top100songs.artist_name FROM spotify2019top LEFT JOIN top100songs ON spotify2019top.Track=top100songs.song_title WHERE top100songs.song_title is not NULL) as moje_zapytanie;")
        total_counts = self.c.fetchall()
        print("In total we have: ",total_counts,"common songs both in Billboard and Spotify ranking")

s=Spotify()
#s.createtabletop100songs()
#s.writeToSQLtable(spotify_data,"TOPsongs_project", "spotify2019top")
s.checkCommonSpotifyAndBillboard()
