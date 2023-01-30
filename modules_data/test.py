from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys



'''
def find_all_links(soup, text, https_link='https://supac.ufba.br/'):
    all_links = []
    for a in soup.find_all('a', href=True):
        a = a.get('href')
        if not a.find(text) == -1:
            if a.find('https') == -1:
                #print('https://supac.ufba.br/' + a)
                all_links.append(https_link + a)
            else:
                #print(a)
                all_links.append(a)
    return all_links



data_links = []
url = 'https://supac.ufba.br/guia-matricula-graduacao'
result = requests.get(url)
doc = BeautifulSoup(result.text, 'html.parser')

text_area = 'guia-de-matricula-por-curso'
for area_link in find_all_links(doc, text_area):
    course_result = requests.get(area_link)
    doc = BeautifulSoup(course_result.text, 'html.parser')
    text_course = '/supac.ufba.br/files/'
    https_set = 'https://supac.ufba.br'
    for item in find_all_links(doc, text_course, https_set):
        data_links.append(item)

sys.setrecursionlimit(10000)

url = data_links[0]
'''

pd.set_option('display.max_rows', None)

test = pd.read_html('https://supac.ufba.br/sites/supac.ufba.br/files/118_16.html', flavor='bs4', encoding='ISO-8859-1', header=[1])[0]

test = test.dropna(how='all').fillna(method='ffill')

print(test)

'''
for item in test:
    print(item)
'''