import pandas as pd

test = pd.read_csv(r'Ufba_flask\data\subject_week.csv', index_col=[0])

a = test['Disciplina'].str.split(pat=' - ', n=1, expand=True)
a.columns = ['Código', 'Disciplina']

test.drop(columns='Disciplina', inplace=True)

test = pd.concat([a,test], axis=1)

print(test)