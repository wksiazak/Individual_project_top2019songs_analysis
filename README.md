#I. Goal  
  Main purpose of this project is to check how similar are the the most popular rankings for 2019: "Billboard" and "Spotify".  The main question is how many songs are both ranked as Top in Billboard's ranking and Top spotify song's ranking as well.  
  After recieving answer on this question the next goal is to apply machine learning alogorithms on dataset which consisst of top Spotify songs from 2010 till 2019.

#II. Steps  
1. I started with creation database in MySQL and checking connection:  
- check of connection is in seperate file ->  sql_check_connection.py  
- I also created class in seperate file which will help in saving data to database -> model_baza_danych.py  

2. Webcrapping data from this page: https://www.billboard.com/charts/year-end/2019/hot-100-songs 
- code is saved in file -> web_scrapping_billboard_100_top_songs.py 

3. 
