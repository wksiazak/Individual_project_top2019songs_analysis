class Top100:
    def __init__ (self,rank, song_title, artist):
        self.rank = rank
        self.song_title = song_title
        self.artist = artist

    def __str__ (self):
        return '| %5s | %100s | %100s |'% \
               (self.rank, self.song_title, self.artist)
