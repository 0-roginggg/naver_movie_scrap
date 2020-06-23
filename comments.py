import requests, time, pdb
from bs4 import BeautifulSoup

base_URL = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?"

def getComments(movie_code, limit = None, sleep = 0.05) :
    # get soup 
    URL = requests.get(base_URL + f"code={movie_code}")
    soup = BeautifulSoup(URL.text, "html.parser")
    
    # check no score
    if isNoScore(soup) :
        return []
    
    # last page_no
    last_page = getLastPage(soup)
    if limit != None :
        last_page = min(last_page, limit)

    comments = []
    for page_no in range(1,last_page + 1) :
        print(f"scarping page {page_no}")        
 
        URL = requests.get(base_URL + f"code={movie_code}" + f"&page={page_no}")
        soup = BeautifulSoup(URL.text, "html.parser")

        comments += getPageComments(soup)
    return comments

def isNoScore(soup) :                                                                             
    is_noScore = soup.find("div", {"class" : "no_score_info"}) != None
    return is_noScore

def getLastPage(soup) :                         
    last_reple_no = int(soup.find("strong").find("em").text.replace(',', ''))
    last_page_no = (last_reple_no // 10) + 1

    return last_page_no

def getPageComments(soup) :
    reples = soup.find('div', {'class' : 'score_result'}).find_all('li')
    comments = []             
    for reple in reples :    
        pdb.set_trace()
        # reple Text 
        repleText = reple.find('div', {'class' : 'score_reple'}).find_all('span')
        # avoid ico_viewer
        if repleText[0].text == "관람객" :    
            repleText = repleText[1].text.strip()
        else :
            repleText = repleText[0].text.strip()
        
        # reple Score
        repleScore = float(reple.find('div', {'class' : 'star_score'}).text)
        
        # reple date
        repleDate = re
        comments.append({
            'text'  : repleText,
            'score' : repleScore
        })
    return comments

