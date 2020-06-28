import requests, time, tqdm, random, pdb
from bs4 import BeautifulSoup
from comments import *
from Error import *
from utility import *
from base_info import *
from detail_info import *

# class 
class MovieInfo : 
    def __init__(self, movieID) :
        # Check if movieID type
        if isinstance(movieID, int) :
            self.movieID = movieID
        else :
            raise DataTypeError('Check Input Data Type')
        # Get Movie Title
        self.list_headers = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                             'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
                             'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
                             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
                             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577']

    # header
    def printHeaders(self) :
        print(self.list_headers)

    def addHeader(self, header) :
        if isinstance(header, list) :
            self.list_headers += header 
        elif isinstance(header, str) :
            self.list_headers.append(header) 
        else :
            raise DataTypeError('Check Input Data Type')
        self.list_headers = list(set(self.list_headers)) # avoid dup


    # comments
    def getComments(self, limit_page = None, tsleep = 0.5, is_random_tsleep = True, header_change = False, header_change_prob = 0.1) :
        headers = {'user-agent' : random.sample(self.list_headers,1)[0]}
        base_URL = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?'   # comments base URL
        
        # get soup
        URL = base_URL + f'code={self.movieID}'
        comments_soup = getSoup(URL, headers = headers)

        # check no score
        if isNoScore(comments_soup) :
            return []

        # last page_no 
        last_page = getLastPage(comments_soup)
        if limit_page is not None :
            last_page = min(last_page, limit_page)
        
        comments = []
        for page_no in tqdm.tqdm(range(1, last_page + 1), desc = f'scarping movie ID | {self.movieID} ') :
            # change header 
            header_change_factor = random.random()
            if (header_change is True) and (header_change_factor < header_change_prob) :
                headers = {'user-agent' : random.sample(self.list_headers,1)[0]}

            # get soup
            URL  = base_URL + f'code={self.movieID}' + f'&page={page_no}'
            comments_soup = getSoup(URL = URL, headers = headers)

            comments += getPageComments(soup = comments_soup)

            # sleep 
            if is_random_tsleep :
                temp_time = random.uniform(tsleep - tsleep * 0.5, tsleep + tsleep * 0.5) 
            else :
                temp_time = tsleep
            time.sleep(temp_time)
        return comments

    # movie base info  
    def getBaseInfo(self) : 
        headers = {'user-agent' : random.sample(self.list_headers,1)[0]}
        URL = f'https://movie.naver.com/movie/bi/mi/basic.nhn?code={self.movieID}'   # comments base URL
        base_info_soup = getSoup(URL = URL, headers = headers)
    
        base_info = {
            'title'             : getTitle(base_info_soup),
            'genres'            : getGenres(base_info_soup),
            'countries'         : getCountry(base_info_soup),
            'running_time'      : getRunningTime(base_info_soup),
            'opening_date'      : getOpeningDate(base_info_soup),
            "director"          : getDirector(base_info_soup),
            'rating'            : getRating(base_info_soup),
            'num_viewer'        : getNumViewer(base_info_soup)
        }
        return base_info

    # detail info
    def getCastList(self) :
        headers = {'user-agent' : random.sample(self.list_headers,1)[0]}
        URL = f'https://movie.naver.com/movie/bi/mi/detail.nhn?code={self.movieID}'   # comments base URL
        cast_soup = getSoup(URL = URL, headers = headers)

        chunks_cast = cast_soup.find('ul', {'class' : 'lst_people'}).find_all('div', {'class', 'p_info'})
        cast_list = [getCast(element) for element in chunks_cast]
        
        return cast_list 
            
    