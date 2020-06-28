import requests, re
from bs4 import BeautifulSoup
from Error import *

# common
def isNoScore(soup) :                                                                             
    is_noScore = soup.find("div", {"class" : "no_score_info"}) != None
    return is_noScore

def getLastPage(soup) :                         
    last_reple_no = int(soup.find("strong").find("em").text.replace(',', ''))
    last_page_no = (last_reple_no // 10) + 1
    return last_page_no

# comment
def getPageComments(soup) :
    chunks_comments = soup.find('div', {'class' : 'score_result'}).find_all('li')
    comments = []             
    for chunk in chunks_comments :   
        comment_score = getCommentScore(chunk)              # score 
        comment_text  = getCommentText(chunk)               # Text 
        comment_date  = getCommentDate(chunk)               # Date
        comment_like, comment_dislike = getNumLike(chunk)   # like & dislike

        comments.append({
            'score'     : comment_score,
            'text'      : comment_text,
            'date'      : comment_date,
            'like'      : comment_like,
            'dislike'   : comment_dislike
        })
    return comments

def getCommentText(soup) :
    comment_text = soup.find('div', {'class' : 'score_reple'}).find_all('span')
    if comment_text[0].text == "관람객" :    
        comment_text = comment_text[1].text.strip()
    else :
        comment_text = comment_text[0].text.strip()
    return comment_text

def getCommentScore(soup) :
    comment_score = float(soup.find('div', {'class' : 'star_score'}).text)
    return comment_score

def getCommentDate(soup) :
    date_text = soup.find('dt').text
    date_text = re.search('[0-9]+.[0-9]+.[0-9]+ [0-9]+:[0-9]+', date_text).group()
    return date_text

def getNumLike(soup) :
    num_like    = soup.find_all('strong')[0].text
    num_dislike = soup.find_all('strong')[1].text
    return num_like, num_dislike

