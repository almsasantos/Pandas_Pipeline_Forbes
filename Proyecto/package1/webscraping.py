import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import requests
from lxml import html
import lxml.html as lh
from bs4 import BeautifulSoup
from acquisition import reading_csv
from cleaning import drop_cols
import os.path

df = reading_csv('df')

def education_list():
    a = list(df.loc[:, 'education'] == 'None')
    count = -1
    none_education_list = []
    for i in a:
        count += 1
        if i == True:
            none_education_list.append(count)
    return none_education_list

def web_scraping_education(df_col):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    page_url = 'https://en.wikipedia.org/wiki/'
    edu_url = []
    for i in education_list(df_col):
        req = requests.get(page_url + df_col[i], headers=header)
        soup = BeautifulSoup(req.text, 'lxml')

        edu_find = soup.find('table', attrs={'class': 'infobox biography vcard'})
        edu_url.append(str(edu_find))

    edu_l = []
    for j in edu_url:
        edu_l.append(re.findall('Alma', j) or re.findall('Education', j))

    edu = []
    for x in edu_l:
        if len(x) != 0:
            edu.append('Yes')
        else:
            edu.append('No')

    edu_df = pd.DataFrame(np.array(edu))
    edu_df.to_csv('edu_csv')

    return edu

def webscraping(file):
    if os.path.exists('edu_csv'):
        edu_data = pd.read_csv('edu_csv')
        df['education'] = edu_data['0']

    else:
        print('This may take a few minutes ...')
        df['education'] = web_scraping_education(df.name)

    return df.to_csv(file,  index=False)


webscraping('df')
