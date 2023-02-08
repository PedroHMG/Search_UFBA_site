import pandas as pd

data_subject_week = pd.read_csv(r'data\subject_week.csv', encoding='ISO-8859-1')
data_subject_week['Turma'] = data_subject_week['Turma'].astype(int).apply(lambda x: '{0:0>6}'.format(x))
data_subject_week = data_subject_week.astype({'Turma': str, 'Vagas Ofe': 'int32'})


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
            data_subject_week.drop(item, inplace=True)
            x += 1
            
#print(data_subject_week)
#print(data_subject_week[data_subject_week.duplicated(subset=['Dia', 'Codigo', 'Turma', 'Docente'], keep=False)])

data_subject_week.to_csv(r'data\subject_week.csv', encoding='ISO-8859-1')
print(x)