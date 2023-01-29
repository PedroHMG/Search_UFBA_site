from sqlalchemy import create_engine, Column, Integer, CHAR, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os


engine = create_engine('sqlite:///./Ufba_flask/data/db.sqlite3', echo=True)
conn = engine.connect()



Base = declarative_base()


class All_collegiate(Base):
    __tablename__ = 'Collegiate'
    row_id = Column("Row_id", Integer, primary_key=True)
    collegiate = Column("Collegiate", Integer)
    subject = Column('Subject', String)
    classes = Column('Classroom', String)
    offered = Column('Offered', Integer)
    demand = Column('Demand', Integer)
    available = Column('Available', Integer)

    def __init__(self, collegiate, subject, classes, offered, demand, available):
        self.collegiate = collegiate
        self.subject = subject
        self.classes = classes
        self.offered = offered
        self.demand = demand
        self.available = available

    def __repr__(self):
        return "Next time"



class Subjects(Base):
    __tablename__ = 'Subjects'
    id = Column('Subject_id', Integer, primary_key=True)
    subject = Column('Subject', String)

    def __init__(self, subject):
        self.subject = subject


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()



dic = os.listdir(r'Ufba_flask\csv_files')
all_pd_data = pd.DataFrame()

#print(dic)


for csv_file in dic:
    temp_read = pd.read_csv(f'Ufba_flask\\csv_files\\{csv_file}', encoding = "ISO-8859-1", index_col=[0], dtype={'Turma': str})
    all_pd_data = pd.concat([all_pd_data, temp_read])

all_pd_data['Disp'] = all_pd_data['Vagas Ofe'] - all_pd_data['Pedidos']


all_subject = all_pd_data.loc[:, ['Disciplina']].drop_duplicates().sort_values('Disciplina').reset_index(drop=True)
print(all_subject)


y = 0
for item in range(len(all_subject.values)):
    df_row = all_subject.iloc[[item]]
    add_row = Subjects(str(df_row['Disciplina'].values[0]))
    session.add(add_row)

y = 0
for item in range(len(all_pd_data.values)):
    df_row = all_pd_data.iloc[[item]]
    add_row = All_collegiate(int(df_row['Colegiado'].values[0]), df_row['Disciplina'].values[0], str(df_row['Turma'].values[0]), 
                        int(df_row['Vagas Ofe'].values[0]), int(df_row['Pedidos'].values[0]), int(df_row['Disp'].values[0]))
    session.add(add_row)

session.commit()
