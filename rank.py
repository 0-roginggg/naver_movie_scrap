import requests, pdb, time, re, progressbar
from bs4 import BeautifulSoup

today = time.strftime('%Y%m%d')
page = 1

# sort by score 
base_URL = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt'

def getMovie() :
    # progress bar define
    bar = progressbar.ProgressBar(maxval = 41, widgets=[' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') ',]).start()

    movie = []
    for page_no in range(1, 41) :
        URL = requests.get(f'{base_URL}&date={today}&page={page_no}')
        soup = BeautifulSoup(URL.text, 'html.parser')

        movie += getPageMovie(soup)

        bar.update(page_no)
    bar.finish()

    return movie

def getPageMovie(soup) :
    rankTable = soup.find('table', {'class':'list_ranking'}).find('tbody').find_all('td', {'class' : 'title'})

    pageMovie = []
    for rankRow in rankTable :
        rankAnchor = rankRow.find('a')
        movieID = int(re.search('code=[0-9]+', rankAnchor['href']).group().replace('code=',''))
        movieTitle = rankAnchor['title']

        pageMovie.append({
            'ID'    : movieID,
            'title' : movieTitle
        })
    return pageMovie
