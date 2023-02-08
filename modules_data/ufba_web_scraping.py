from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import time
from sqlalchemy import create_engine, Column, Integer, CHAR, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os



engine = create_engine('sqlite:///./Ufba_flask/data/db.sqlite3', echo=True)
conn = engine.connect()


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


data_subject_week['Turma'] = data_subject_week['Turma'].astype(int).apply(lambda x: '{0:0>6}'.format(x))
data_subject_week = data_subject_week.astype({'Turma': str, 'Vagas Ofe': 'int32'})
data_subject_week.drop_duplicates(inplace=True)

divided_column = data_subject_week['Disciplina'].str.split(pat=' - ', n=1, expand=True)
divided_column.columns = ['Codigo', 'Disciplina']
data_subject_week.drop(columns='Disciplina', inplace=True)
data_subject_week = pd.concat([divided_column,data_subject_week], axis=1)

data_subject_week.rename(columns={"Horário": "Horario"}, inplace=True)

#data_subject_week['Horario'] = data_subject_week['Horario'].str.replace('às','as')

data_subject_week = data_subject_week.drop_duplicates(subset=['Turma', 'Dia', 'Horario', 'Docente'])




data_subject_week[['Inicio', 'Fim']] = data_subject_week['Horario'].str.split(' às ', expand=True)
pd.set_option('display.max_rows', 500)

x = 0
for item in range(len(data_subject_week.index) -1, 0, -1):
    first_row = data_subject_week.iloc[item]
    second_row = data_subject_week.iloc[item - 1]
    first_word = first_row['Inicio']
    last_word = second_row['Fim']

    if first_row.loc[['Codigo', 'Turma', 'Dia', 'Docente']].equals(second_row.loc[['Codigo', 'Turma', 'Dia', 'Docente']]):
        if first_word == last_word:
            data_subject_week.loc[item - 1, 'Fim'] = first_row.loc['Fim']
            data_subject_week.drop(first_row, inplace=True)
            x += 1
            
#print(data_subject_week)
#print(data_subject_week[data_subject_week.duplicated(subset=['Dia', 'Codigo', 'Turma', 'Docente'], keep=False)])
print(x)


print(data_subject_week)
data_subject_week.to_csv(r'Ufba_flask\data\subject_week.csv', encoding='ISO-8859-1', index=False)

#should add funcionalty to remove all duplicaded day of the week to one subject-class because of broken ufba site 
#se o horário que finaliza for igual ao primeiro do outro adiciona um ao outro
