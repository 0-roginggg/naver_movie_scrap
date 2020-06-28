import requests, re
from bs4 import BeautifulSoup

def getCast(soup) :
    cast = {
        'k_name'           : soup.find('a', {'class' : 'k_name'}).text ,
        'e_name'           : soup.find('em', {'class' : 'e_name'}).text ,
        'classification'   : soup.find('p', {'class' : 'in_prt'}).text.strip() ,
        'casting_name'     : soup.find('p', {'class' : 'pe_cmt'}).text.strip()
    }
    return cast