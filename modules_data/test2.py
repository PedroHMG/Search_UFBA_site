import pandas as pd

data_subject_week = pd.read_csv(r'Ufba_flask\data\subject_week.csv', encoding='ISO-8859-1')
data_subject_week['Turma'] = data_subject_week['Turma'].astype(int).apply(lambda x: '{0:0>6}'.format(x))
data_subject_week = data_subject_week.astype({'Turma': str, 'Vagas Ofe': 'int32'})


data_subject_week[['Inicio', 'Fim']] = data_subject_week['Horario'].str.split(' às ', expand=True)


while not data_subject_week[data_subject_week.duplicated(subset=['Dia', 'Codigo', 'Turma', 'Docente'], keep=False)].empty:
    print(123)
    duppe_bolean = data_subject_week.duplicated(subset=['Dia', 'Codigo', 'Turma', 'Docente'], keep='first')
    duppe_bolean = - duppe_bolean
    duppe = data_subject_week[- duppe_bolean]
    duppe_all = data_subject_week[data_subject_week.duplicated(subset=['Dia', 'Codigo', 'Turma', 'Docente'], keep=False)]

    duppe = duppe['Fim']
    duppe.index = duppe.index - 1
    #print(duppe)
    #print(duppe_all)
    print(duppe)


    data_subject_week.loc[duppe.index, 'Fim'] = duppe


    data_subject_week = data_subject_week[duppe_bolean]
    #print(data_subject_week[data_subject_week.duplicated(subset=['Dia', 'Codigo', 'Turma', 'Docente'], keep=False)])
    data_subject_week.reset_index(drop=True)
    print(data_subject_week)
    
    input()

print(data_subject_week[data_subject_week.duplicated(subset=['Dia', 'Codigo', 'Turma', 'Docente'], keep=False)])
'''


test = data_subject_week.shift(-1, fill_value = False)
print(data_subject_week)
print(test)
'''


'''
for item in range(len(data_subject_week['Horario']) -1, 0, -1):  
    if data_subject_week.iloc[item]['Bolean'] == False:
        data_subject_week.iloc[item]['Horario'].str.replace()

'''

'''

for item in range(len(data_subject_week['Horario']) - 1, 1, -1):
    print(item)
    if data_subject_week.iloc[item][['Codigo', 'Turma', 'Dia']] == data_subject_week.iloc[item - 1][['Codigo', 'Turma', 'Dia']]
        print('x')

'''
'''
print(duppe)
print(first_word.compare(last_word, keep_equal=False))
'''
#print((last_word))
#print(first_word)

