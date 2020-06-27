import requests, pdb, re
from bs4 import BeautifulSoup
from Error import *

# util
def isNoScore(soup) :                                                                             
    is_noScore = soup.find("div", {"class" : "no_score_info"}) != None
    return is_noScore

def getLastPage(soup) :                         
    last_reple_no = int(soup.find("strong").find("em").text.replace(',', ''))
    last_page_no = (last_reple_no // 10) + 1
    return last_page_no

def getSoup(URL, headers = None) : 
    web_request = requests.get(URL, headers = headers)
    if web_request.status_code == 200 :
        soup = BeautifulSoup(web_request.text, "html.parser")
        return soup
    else :
        raise ResponseError("Response Error")
    # add 403 forbidden 

# comment
def getPageComments(soup) :
    reples = soup.find('div', {'class' : 'score_result'}).find_all('li')
    comments = []             
    for reple in reples :   
        reple_score = getRepleScore(reple)              # score 
        reple_text  = getRepleText(reple)               # Text 
        reple_date  = getRepleDate(reple)               # Date
        reple_like, reple_dislike = getNumLike(reple)   # like & dislike

        comments.append({
            'score'     : reple_score,
            'text'      : reple_text,
            'date'      : reple_date,
            'like'      : reple_like,
            'dislike'   : reple_dislike
        })
    return comments

def getRepleText(reple) :
    reple_text = reple.find('div', {'class' : 'score_reple'}).find_all('span')
    if reple_text[0].text == "관람객" :    
        reple_text = reple_text[1].text.strip()
    else :
        reple_text = reple_text[0].text.strip()
    return reple_text

def getRepleScore(reple) :
    reple_score = float(reple.find('div', {'class' : 'star_score'}).text)
    return reple_score

def getRepleDate(reple) :
    date_text = reple.find('dt').text
    date_text = re.search('[0-9]+.[0-9]+.[0-9]+ [0-9]+:[0-9]+', date_text).group()
    return date_text

def getNumLike(reple) :
    num_like    = reple.find_all('strong')[0].text
    num_dislike = reple.find_all('strong')[1].text
    return num_like, num_dislike

