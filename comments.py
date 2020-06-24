import requests, time, progressbar, random
from bs4 import BeautifulSoup

base_URL = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?"

def getComments(movie_code, limitPage = None, tSleep = 0.05, header_change = False, headerChangeProb = 0.1) :
    listHeaders = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577')
    headers = {'user-agent' : random.sample(listHeaders,1)[0]}
    
    # get soup 
    URL  = requests.get(base_URL + f"code={movie_code}", headers = headers)
    soup = BeautifulSoup(URL.text, "html.parser")
    
    # check no score
    if isNoScore(soup) :
        return []
    
    # last page_no
    last_page = getLastPage(soup)
    if limitPage != None :
        last_page = min(last_page, limitPage)

    # progress bar define
    bar = progressbar.ProgressBar(maxval = last_page + 1, widgets=[' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') ',]).start()

    comments = []
    for page_no in range(1,last_page + 1) :
        # change header 
        randHeaderChg = random.random()
        if (header_change == True) and (randHeaderChg < headerChangeProb) :
            headers = {'user-agent' : random.sample(listHeaders,1)[0]}
    
        URL = requests.get(base_URL + f"code={movie_code}" + f"&page={page_no}", headers = headers)
        soup = BeautifulSoup(URL.text, "html.parser")

        comments += getPageComments(soup, tSleep)
        bar.update(page_no)
    bar.finish()

    return comments

def isNoScore(soup) :                                                                             
    is_noScore = soup.find("div", {"class" : "no_score_info"}) != None
    return is_noScore

def getLastPage(soup) :                         
    last_reple_no = int(soup.find("strong").find("em").text.replace(',', ''))
    last_page_no = (last_reple_no // 10) + 1

    return last_page_no

def getPageComments(soup, tSleep) :
    reples = soup.find('div', {'class' : 'score_result'}).find_all('li')
    comments = []             
    for reple in reples :    
        # reple Text 
        repleText = reple.find('div', {'class' : 'score_reple'}).find_all('span')
        # avoid ico_viewer
        if repleText[0].text == "관람객" :    
            repleText = repleText[1].text.strip()
        else :
            repleText = repleText[0].text.strip()
        
        # reple Score
        repleScore = float(reple.find('div', {'class' : 'star_score'}).text)
        
        comments.append({
            'text'  : repleText,
            'score' : repleScore
        })

        # sleep
        time.sleep(tSleep)
    return comments