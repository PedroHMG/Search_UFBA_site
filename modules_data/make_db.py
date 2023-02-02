from sqlalchemy import create_engine, Column, Integer, CHAR, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd
import os
import time

engine = create_engine('sqlite:///./Ufba_flask/data/db.sqlite3')
conn = engine.connect()

Base = declarative_base()

collegiate_week_subject = Table( 
    "association_week_colegiate",
    Base.metadata,
    Column('Collegiate_row_id', Integer, ForeignKey('Collegiate.Row_id')),
    Column('week_subject_id', Integer, ForeignKey('Week_subject.Subject_id'))
)


class All_collegiate(Base):
    __tablename__ = 'Collegiate'
    row_id = Column("Row_id", Integer, primary_key=True)
    collegiate = Column("Collegiate", Integer)
    subject = Column('Subject', String)
    classes = Column('Classroom', String)
    offered = Column('Offered', Integer)
    demand = Column('Demand', Integer)
    available = Column('Available', Integer)
    week = relationship('Week_subject', secondary=collegiate_week_subject, backref='demand_offert')

    def __init__(self, collegiate, subject, classes, offered, demand, available):
        self.collegiate = collegiate
        self.subject = subject
        self.classes = classes
        self.offered = offered
        self.demand = demand
        self.available = available

    def __repr__(self):
        return "working on..."



class Week_subject(Base):
    __tablename__ = 'Week_subject'
    id = Column('Subject_id', Integer, primary_key=True)
    code = Column('Subject', String)
    subject_name = Column('Subject_name', String)
    classes = Column('Classes', String)
    day_of_week = Column('Day_of_week', String)
    schedule = Column('Schedule', String)
    professor = Column('Professor', String)

    def __init__(self, code, subject_name, classes, day_of_week, schedule, professor):
        self.code = code
        self.subject_name = subject_name
        self.classes = classes
        self.day_of_week = day_of_week
        self.schedule = schedule
        self.professor = professor

    def __repr__(self):
        return f'<id: {self.id}> <code: {self.code}> <subject_name: {self.subject_name}> <classes: {self.classes}> <day_of_week: {self.day_of_week}> <schedule: {self.schedule}> <professor:  {self.professor}>'


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


dic = os.listdir(r'Ufba_flask\csv_files')
all_pd_data = pd.DataFrame()

for csv_file in dic:
    temp_read = pd.read_csv(f'Ufba_flask\\csv_files\\{csv_file}', encoding = "ISO-8859-1", index_col=[0], dtype={'Turma': str})
    all_pd_data = pd.concat([all_pd_data, temp_read])

all_pd_data['Disp'] = all_pd_data['Vagas Ofe'] - all_pd_data['Pedidos']


all_week_subject = pd.read_csv(r'Ufba_flask\data\subject_week.csv', encoding='ISO-8859-1', index_col=[0])
all_week_subject['Turma'] = all_week_subject['Turma'].astype(int)
all_week_subject['Turma'] = all_week_subject['Turma'].apply(lambda x: '{0:0>6}'.format(x))
all_week_subject = all_week_subject.astype({'Turma': str, 'Vagas Ofe': 'int32'})


y = 0
x = 0
for item in range(len(all_pd_data.values)):
    df_row = all_pd_data.iloc[[item]]
    add_row = All_collegiate(int(df_row['Colegiado'].values[0]), df_row['Disciplina'].values[0], str(df_row['Turma'].values[0]), 
                        int(df_row['Vagas Ofe'].values[0]), int(df_row['Pedidos'].values[0]), int(df_row['Disp'].values[0]))

    '''
    print(str(df_row['Turma'].values[0]), df_row['Disciplina'].values[0])
    append_to_df_row = all_week_subject[(all_week_subject['Codigo'] == str(df_row['Disciplina'].values[0]))]
    print(append_to_df_row)
    time.sleep(0.5)
    if append_to_df_row.empty:
        print('DataFrame is empty!')
        y += 1
    '''

    session.add(add_row)
        
#quantity of classas that don't exit no more
#print(y)
#exit()

y = 0
x = 0
for item in range(len(all_week_subject.values)):
    df_row = all_week_subject.iloc[[item]]
    add_row = Week_subject(str(df_row['Codigo'].values[0]), str(df_row['Disciplina'].values[0]), str(df_row['Turma'].values[0]), 
                str(df_row['Dia'].values[0]), str(df_row['Horario'].values[0]), str(df_row['Docente'].values[0]))
    session.add(add_row)


for colle in session.query(All_collegiate):
    query_week = session.query(Week_subject).filter(
        Week_subject.code.like(colle.subject),
        Week_subject.classes.like(colle.classes)
    )
    for item in query_week:
        colle.week.append(item)

        
    
session.commit()

