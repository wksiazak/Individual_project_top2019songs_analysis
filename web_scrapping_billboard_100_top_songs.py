import requests
import pymysql
from bs4 import BeautifulSoup
from model_baza_danych import Top100

class BillboardScrapper:

    def gettop100songs2019(self):
        try:
            self.page = requests.get("https://www.billboard.com/charts/year-end/2019/hot-100-songs")
            print("Wykonano poprawnie żadanie")
        except:
            print("Cos jest nie tak")

    def __init__(self):
        self.topsongs2019 = []
        user = "TOPsongs_project_user"
        password = "qwerty1234"
        self.conn = pymysql.connect("localhost", user, password, "TOPsongs_project")
        self.c =self.conn.cursor()

    def scrappingTOP100songs2019(self):
        html_content = BeautifulSoup(self.page.content, 'html.parser')
        ranks = html_content.find_all(class_ = "ye-chart-item__rank")
        song_titles = html_content.find_all(class_ = "ye-chart-item__title")
        artist_names= html_content.find_all(class_ = "ye-chart-item__artist")

        for index, artist_name in enumerate(artist_names):
            #if (index==10):
                #break
            song_titles[index] = str(song_titles[index]).split(">")[1].replace("\n","").split("<")[0]
            ranks[index]=str(ranks[index]).split(">")[1].split("<")[0].replace("\n","")


            artist_names[index]= str(artist_names[index]).replace("ye-chart-item__artist","").replace("href","").replace("<div class=","").replace(">\n<a ","").split(">\n")[1].replace("\n</a","").replace("\n</div>","")
            songs2019 = Top100(ranks[index], song_titles[index],artist_names[index])
            print(songs2019)
            self.topsongs2019.append(songs2019)

    def createtabletop100songs(self):
        self.c.execute("create table top100songs("
                       "id_number int primary key auto_increment,"
                       "rank_no varchar(10),"
                       "song_title varchar(255),"
                       "artist_name varchar(255))")
        self.conn.commit()

    def saveSongsToDatabase(self):
        for song in self.topsongs2019:
            self.c.execute("INSERT INTO top100songs VALUES (default, %s, %s, %s)",
                           (song.rank, song.song_title, song.artist))
        self.conn.commit()
        print("Dodano piosenki do tabeli")
        self.conn.close()


billboard = BillboardScrapper()
billboard.gettop100songs2019()
billboard.scrappingTOP100songs2019()
billboard.createtabletop100songs()
billboard.saveSongsToDatabase()
