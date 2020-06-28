import requests
from bs4 import BeautifulSoup

def getSoup(URL, headers = None) : 
    web_request = requests.get(URL, headers = headers)
    if web_request.status_code == 200 :
        soup = BeautifulSoup(web_request.text, "html.parser")
        return soup
    else :
        raise ResponseError("Response Error")
    # add 403 forbidden 
