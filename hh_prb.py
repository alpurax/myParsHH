# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import pprint

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
base_url = 'https://hh.ru/search/vacancy?area=1&search_period=7&text=python&page=0'

def hh_print(parsjobs):
    for job in parsjobs:
        #pprint.pprint(job)
        print('Title: ',job['title'])
        print('Salary: ',job['Salary'])
        print(job['href'])
        print(job['company'])
        pprint.pprint(job['content'])
        print('== *** ==')

def hh_parse(base_url, headers):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a',attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            try:
                summ = int(''.join(filter(str.isdigit,div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text)))
            except:
                summ = 'Не указано'
            text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = text1+ ' '+text2
            jobs.append({
                'title': title,
                'href': href,
                'Salary': summ,
                'company': company,
                'content': content
            })
        hh_print(jobs)
        print('\nВсего:',len(jobs),'записей.')
    else:
        print('ERROR')

hh_parse(base_url, headers)