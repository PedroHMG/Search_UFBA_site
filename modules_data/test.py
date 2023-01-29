import pandas as pd
import os


dic = os.listdir(r'Ufba_flask\csv_files')
all_pd_data = pd.DataFrame()

#print(dic)


for csv_file in dic:
    temp_read = pd.read_csv(f'Ufba_flask\\csv_files\\{csv_file}', encoding = "ISO-8859-1", index_col=[0], dtype={'Turma': str})
    all_pd_data = pd.concat([all_pd_data, temp_read])

all_pd_data['Disp'] = all_pd_data['Vagas Ofe'] - all_pd_data['Pedidos']

pd.set_option('display.max_rows', None)

all_subject = all_pd_data['Disciplina'].drop_duplicates().sort_values().reset_index(drop=True)


print(all_subject)