import requests
from bs4 import BeautifulSoup

base_URL = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?"

def getComments(movie_code, skip_empty_comment = False) :
    URL = requests.get(base_URL + f"code={movie_code}")
    soup = BeautifulSoup(URL.text, "html.parser")
    
    # check no score
    if isNoScore(soup) :
        return None

    last_page = getLastPage(soup)
    comments = []
    for page_no in range(1,last_page + 1) :
        print(f"scarping page {page_no}")        
 
        URL = requests.get(base_URL + f"code={movie_code}" + f"&page={page_no}")
        soup = BeautifulSoup(URL.text, "html.parser")
        comments += getPageComments(soup, skip_empty_comment)

    return comments

def isNoScore(soup) :                                                                             
    is_noScore = soup.find("div", {"class" : "no_score_info"}) != None
    return is_noScore

def getLastPage(soup) :                         
    last_reple_no = int(soup.find("strong").find("em").text.replace(',', ''))
    last_page_no = (last_reple_no // 10) + 1

    return last_page_no

def getPageComments(soup, skip_empty_comment) :
    reples = soup.find_all("div", {"class": "score_reple"})

    comments = []             
    for reple in reples :
        comment = reple.find_all("span")

        # avoid ico_viewer
        if comment[0].text == "관람객" :    
            comment = comment[1].text.strip()
        else :
            comment = comment[0].text.strip()

        # avoid empty comment
        if (comment == "") and (skip_empty_comment) :
            continue

        comments.append(comment)

    return comments