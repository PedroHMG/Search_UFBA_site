import pandas as pd
from tabulate import tabulate
import os


num = 101
list = []
while num < 888:
    list_num = 0

    pdf_name = 'Collegiate_{}'.format(num)
    path_to_csv = 'csv_files\\{}.csv'.format(pdf_name)
    #print(num)

    if os.path.isfile(path_to_csv):
        df = pd.read_csv(path_to_csv, encoding='cp1252', index_col=0)
        df['Turma'] = df['Turma'].apply(lambda x: '{0:0>6}'.format(x))

        dis_value = 'ECOB40'
        local = df.loc[df['Disciplina'] == dis_value]

        if not local.empty:
            list.append(local)

    num += 1

df_result = pd.concat(list)


df_vagas = df_result['Vagas Ofe'] - df_result['Pedidos']
df_result['Vagas disp'] = df_vagas
df_result = df_result.sort_values(by=['Colegiado'], ascending=False)

print(df_result)
