import csv, pickle, random
from rank import *
from comments import *

movies = getMovie()
movies = movies[0:200]

rank = 1

for movie in movies :
    table = []
    movieID = movie['ID']
    movieTitle = movie['title']

    print(f'scarping movie : {movieTitle} (rank = {rank})')
    # random sleep time 
    sleep_time = round(random.random(),1) / 10
    comments = getComments(movieID, 
                           tSleep = sleep_time, 
                           header_change = True, 
                           headerChangeProb = 0.02)

    table.append({
        'ID' : movieID,
        'TITLE' : movieTitle,
        'COMMENTS' : comments
    })

    # save
    with open(f'movie_comments/{movieID}.pickle', 'wb') as movie_file :
        pickle.dump(table, movie_file)


    rank += 1
