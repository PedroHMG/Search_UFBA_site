from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import time


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


pd.set_option('display.max_rows', 500)

data_subject_week = pd.DataFrame()
for link in data_links:
    time.sleep(0.1)
    data = pd.read_html(link, flavor='bs4', encoding='ISO-8859-1', header=[1])[0]
    data = data.dropna(how='all').fillna(method='ffill')
    data_subject_week = pd.concat([data_subject_week, data])


data_subject_week['Turma'] = data_subject_week['Turma'].astype(int)
data_subject_week = data_subject_week.astype({'Turma': str, 'Vagas Ofe': 'int32'})
data_subject_week.drop_duplicates(inplace=True)

divided_column = data_subject_week['Disciplina'].str.split(pat=' - ', n=1, expand=True)
divided_column.columns = ['Código', 'Disciplina']
data_subject_week.drop(columns='Disciplina', inplace=True)
data_subject_week = pd.concat([divided_column,data_subject_week], axis=1)

print(data_subject_week)
data_subject_week.to_csv(r'Ufba_flask\data\subject_week.csv')
