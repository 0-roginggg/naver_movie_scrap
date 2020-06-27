import requests, time, tqdm, random, pdb
from bs4 import BeautifulSoup
from comments import *
from Error import *

# class 
class NaverMovieInfo : 
    def __init__(self, movieID) :
        # Check if movieID type
        if isinstance(movieID, int) :
            self.movieID = [movieID]
        elif isinstance(movieID, list) :
            self.movieID = movieID
        else :
            raise DataTypeError("Check Input Data Type")
        # Get Movie Title
        self.list_headers = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                             'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
                             'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
                             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
                             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577']
    
    def addMovieID(self, additionalID) :
        if isinstance(additionalID, list) :
            self.movieID += additionalID 
        elif isinstance(additionalID, int) :
            self.movieID.append(additionalID) 
        else :
            raise DataTypeError("Check Input Data Type")
        self.movieID = list(set(self.movieID))          # avoid dup

    # header
    def printHeaders(self) :
        print(self.list_headers)

    def addHeader(self, header) :
        if isinstance(header, list) :
            self.list_headers += header 
        elif isinstance(header, str) :
            self.list_headers.append(header) 
        else :
            raise DataTypeError("Check Input Data Type")
        self.list_headers = list(set(self.list_headers)) # avoid dup


    # comments
    def getComments(self, limit_page = None, tsleep = 0.5, is_random_tsleep = True, header_change = False, header_change_prob = 0.1) :
        headers = {'user-agent' : random.sample(self.list_headers,1)[0]}
        base_URL = "https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?"   # comments base URL
        
        bag_comments = {}
        for mID in self.movieID :
            print(f'scarping movie ID : {mID}')
            # get soup
            URL = base_URL + f"code={mID}"
            soup = getSoup(URL, headers = headers)

            # check no score
            if isNoScore(soup) :
                pass

            # last page_no 
            last_page = getLastPage(soup)
            if limit_page != None :
                last_page = min(last_page, limit_page)
            
            comments = []
            for page_no in tqdm.tqdm(range(1, last_page + 1)) :
                # change header 
                header_change_factor = random.random()
                if (header_change == True) and (header_change_factor < header_change_prob) :
                    headers = {'user-agent' : random.sample(self.list_headers,1)[0]}

                # get soup
                URL  = base_URL + f"code={mID}" + f"&page={page_no}"
                soup = getSoup(URL = URL, headers = headers)

                comments += getPageComments(soup = soup)

                # sleep 
                if is_random_tsleep == True :
                    temp_time = random.uniform(tsleep - tsleep * 0.5, tsleep + tsleep * 0.5) 
                else :
                    temp_time = tsleep
                time.sleep(temp_time)

            bag_comments[mID] = comments

        return bag_comments