import requests, re, pdb
from bs4 import BeautifulSoup

def getTitle(soup) :
    title = soup.find('h3', {'class' : 'h_movie'}).find('a').text
    return title

def getGenres(soup) :
    list_genre = soup.find('dl', {'class' : 'info_spec'}).find_all('dd')[0].find_all('span')[0].find_all('a')
    genres = [element.text for element in list_genre]
    return genres

def getCountry(soup) :
    list_country = soup.find('dl', {'class' : 'info_spec'}).find_all('dd')[0].find_all('span')[1].find_all('a')
    countries = [element.text for element in list_country]
    return countries

def getRunningTime(soup) :
    running_time = soup.find('dl', {'class' : 'info_spec'}).find_all('dd')[0].find_all('span')[2].text
    running_time = int(re.search('[0-9]+', running_time).group())
    return running_time

def getOpeningDate(soup) :
    chunks_opening_date = soup.find('dl', {'class' : 'info_spec'}).find_all('dd')[0].find_all('span')
    if len(chunks_opening_date) < 4 :
        return -1             
    chunks_opening_date = chunks_opening_date[3].text
    list_opening_date = re.findall('[0-9]+\n.[0-9]+.[0-9]+', chunks_opening_date)

    opening_date = [element.replace('n','') for element in list_opening_date]
    return opening_date

def getDirector(soup) :
    director = soup.find('dl', {'class' : 'info_spec'}).find_all('dd')[1].text
    return director

def getRating(soup) : 
    rating = soup.find('dl', {'class' : 'info_spec'}).find_all('dd')[3].find_all('a')[0].text
    # 해외 관람 등급 추가
    return rating

def getNumViewer(soup) :
    num_viewer = soup.find('dl', {'class' : 'info_spec'}).find('p', {'class' : 'count'})
    if num_viewer is None :
        num_viewer = -1
    else : 
        num_viewer = num_viewer.text
        num_viewer = num_viewer[:num_viewer.find('명')].replace(',', '')
        num_viewer = int(num_viewer)
    return num_viewer

# 추가 필요
# def getIsNowPlaying(soup) :
#    pass