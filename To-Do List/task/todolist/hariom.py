from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todoe.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return  self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
today = Session()
current_day = datetime.today()
gulab = True
def todays():
    rows = today.query(Table).all()
    if len(rows) == 0:
        print(f'Today {current_day.day} {current_day.strftime("%b")}:\nNothing to do!\n')
    else:
        for i in range(len(rows)):
            row = rows[i]
            print(f'{row.id}. {row.task}')
def all_task():
    row = today.query(Table).order_by(Table.deadline).all()
    for i in range(len(row)):
        raw = row[i]
        print(f'{raw.id}. {raw.task}. {raw.deadline.day} {raw.deadline.strftime("%b")}')
def weektask():
    toDay = current_day.day
    moNth = current_day.strftime("%b")
    weeK = current_day.weekday()
    for i in range(7):
        tom = current_day.now()
        cu = tom+timedelta(days=i)
        name = cu.strftime('%A')
        rdws = today.query(Table).filter(Table.deadline == cu.date()).all()
        if len(rdws) == 0:
            print(f'{name} {cu.day} {cu.strftime("%b")}:\nNothing to do!\n')
        else:
            for i in range(len(rdws)):
                print(f'{name} {cu.day} {moNth}')
                print(f'{i+1}. {rdws[i]}')
                print()
def missedtask():
    tom = current_day.now()
    toDay = current_day.day
    moNth = current_day.strftime("%b")
    rdwsr = today.query(Table).filter(Table.deadline < tom.date()).all()
    print('Missed tasks:')
    if len(rdwsr) == 0:
        print('The task has been deleted!')
    else:
        for i in range(len(rdwsr)):
            print(f'{i + 1}. {rdwsr[i]} {rdwsr[i].deadline.day} {rdwsr[i].deadline.strftime("%b")}')

def deletetask():
    rowe = today.query(Table).order_by(Table.deadline).all()
    print('Choose the number of the task you want to delete:')
    for i in range(len(rowe)):
        raw = rowe[i]
        print(f'{raw.id}. {raw.task}. {raw.deadline.day} {raw.deadline.strftime("%b")}')
    dele = rowe[int(input()) - 1]
    today.delete(dele)
    today.commit()
    print('The task has been deleted!')
while gulab:
    activity = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    if activity == '1':
        todays()
    elif activity == '5':
        ss = input('Enter task\n')
        dd = input('Enter deadline\n')
        #date_field = datetime.strptime('01-24-2020', '%m-%d-%Y')
        dead = datetime.strptime(dd, '%Y-%m-%d').date()
        tk = Table(task=ss, deadline=dead)
        today.add(tk)
        today.commit()
    elif activity == '3':
        all_task()
    elif activity == '2':
        weektask()
    elif activity == '4':
        missedtask()
    elif activity == '6':
        deletetask()
    else:
        print('Bye!')
        gulab = False






