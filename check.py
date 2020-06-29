import pandas as pd

hot100_df = pd.read_csv('https://query.data.world/s/qf6et5c7dh23kglnvjcoztlmom62it')
hot100_df.drop_duplicates(subset='SongID', inplace = True) #remove duplicate occurrences of songs
hot100_df.reset_index()

pd.set_option('display.max_columns', None)

print (hot100_df.head())
