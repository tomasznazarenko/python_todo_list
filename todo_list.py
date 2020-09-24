from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

menu = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""


def print_today_tasks():
    today = datetime.today()
    day = today.day
    month_shortened = today.strftime('%b')
    rows = session.query(Task).filter(Task.deadline == today.date()).all()
    print()
    print(f'Today {day} {month_shortened}:')
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for row in rows:
            print(row)
    print()


def print_weeks_tasks():
    weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    today = datetime.today()
    next_week = today + timedelta(days=7)
    rows = session.query(Task).order_by(Task.deadline).filter(Task.deadline.between(today.date(), next_week.date())).all()
    print()

    weekdays_tasks = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    for row in rows:
        weekdays_tasks[row.deadline.weekday()].append(row)

    tasks_day = datetime.today()
    day_count = range(7)
    for _ in day_count:
        day_string = weekdays.get(tasks_day.weekday())
        day_number = tasks_day.day
        month_shortened = tasks_day.strftime('%b')
        tasks = weekdays_tasks[tasks_day.weekday()]
        print(f"{day_string} {day_number} {month_shortened}:")
        if len(tasks) == 0:
            print("Nothing to do!")
        for index, task in enumerate(tasks):
            print(f"{index + 1}. {task}")
        print()
        tasks_day = (tasks_day + timedelta(days=1))
    print()


def print_all_tasks():
    rows = session.query(Task).order_by(Task.deadline).all()
    print()
    print(f'All tasks')
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for row in rows:
            day_number = row.deadline.day
            month_shortened = row.deadline.strftime('%b')
            print(f'{row}. {day_number} {month_shortened}')
    print()


def print_missed_tasks():
    rows = session.query(Task).filter(Task.deadline < datetime.today()).order_by(Task.deadline).all()
    print()
    print(f'Missed tasks')
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        for index, row in enumerate(rows):
            day_number = row.deadline.day
            month_shortened = row.deadline.strftime('%b')
            print(f'{index + 1}. {row}. {day_number} {month_shortened}')
    print()


def delete_task():
    print("Choose the number of the task you want to delete:")
    rows = session.query(Task).filter(Task.deadline < datetime.today()).order_by(Task.deadline).all()
    if len(rows) == 0:
        print("Nothing to delete")
    else:
        for index, row in enumerate(rows):
            day_number = row.deadline.day
            month_shortened = row.deadline.strftime('%b')
            print(f'{index + 1}. {row}. {day_number} {month_shortened}')
        task_index_to_delete = int(input()) - 1
        specific_row = rows[task_index_to_delete]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")


def add_task():
    print("Enter task")
    task = input()
    print("Enter deadline")
    deadline_str = input()
    deadline = datetime.strptime(deadline_str, '%Y-%m-%d')  # Format example: '2020-04-24'
    new_row = Task(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


while True:
    print(menu)
    option = int(input())
    if option == 0:
        break
    if option == 1:
        print_today_tasks()
    elif option == 2:
        print_weeks_tasks()
    elif option == 3:
        print_all_tasks()
    elif option == 4:
        print_missed_tasks()
    elif option == 5:
        add_task()
    elif option == 6:
        delete_task()

print()
print("Bye!")



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Date
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime, timedelta
# 
# # initialising the parent class for a table
# Base = declarative_base()
# 
# 
# # a task table
# class Task(Base):
#     __tablename__ = "task"
#     id = Column(type_=Integer, primary_key=True, autoincrement=True)
#     task = Column(type_=String)
#     deadline = Column(type_=Date, default=datetime.today().date())
# 
#     def __repr__(self):
#         """
#         it will look like this format
#         id. task
#         id. task
#         """
#         return f"{self.task}"
# 
# 
# class ToDoList:
# 
#     def __init__(self, db_name: str):
#         """
#         initialising the database and gui
#         """
#         # table and database initialising
#         self.engine = create_engine(f"sqlite:///{db_name}.db?check_same_thread=False")
#         Base.metadata.create_all(self.engine)
# 
#         # Session and interaction with database initialising
#         self.session = sessionmaker(bind=self.engine)()
# 
#         # todo list gui initialising
#         self.prompt = "\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n" + \
#                       "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n"
#         self.choices = {'1': self.get_day_tasks,
#                         '2': self.get_week_tasks,
#                         '3': self.get_all_tasks,
#                         '4': self.missed_tasks,
#                         '5': self.add_task,
#                         '6': self.delete_task,
#                         '0': self.shutdown}
#         self.running = True
#         self.main()
# 
#     def shutdown(self) -> None:
#         """
#         shuts down the program, by terminating the while loop
#         """
#         print('Bye!')
#         self.running = False
# 
#     def get_day_tasks(self, day=datetime.today().date(), today=True) -> None:
#         """
#         acquires all the records for today in the database
#         """
#         tasks = self.session.query(Task).filter(Task.deadline == day).all()
#         print(f'Today {day.strftime("%d %b")}:' if today else
#               f'{day.strftime("%A %d %b")}:')
#         self.print_tasks(tasks=tasks)
# 
#     def get_week_tasks(self) -> None:
#         """
#         acquires all the records for this week in the database
#         """
#         # print starting with sunday
#         for i in range(0, 7):
#             self.get_day_tasks(day=datetime.today().date() + timedelta(days=i), today=False)
#             print()
# 
#     def get_all_tasks(self) -> None:
#         """
#         acquires all the records in the database
#         """
#         tasks = self.session.query(Task).order_by(Task.deadline).all()
#         print("All tasks:")
#         self.print_tasks(tasks=tasks, for_a_day=False)
#         
#     @staticmethod
#     def print_tasks(tasks: list, for_a_day=True) -> None:
#         """
#         if there are no tasks:
#             it will prompt it
#         else:
#             it will print them one by one, in an appropriate format
#         """
#         if tasks:
#             for i, task in enumerate(tasks, start=1):
#                 print(f'{i}) {task}' if for_a_day else
#                       f'{i}. {task}. {task.deadline.strftime("%d %b")}')
#         else:
#             print("Nothing to do!")
# 
#     def add_task(self) -> None:
#         """
#         adds a task to the database
#         """
#         task = input('Enter task\n')
#         deadline = datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d')
#         self.session.add(Task(task=task, deadline=deadline))
#         self.session.commit()
#         print("The task has been added!")
# 
#     def delete_task(self) -> None:
#         """
#         deletes the chosen task. Print 'Nothing to delete' if the tasks list is empty.
#         """
#         tasks = self.session.query(Task).order_by(Task.deadline).all()
#         print('Choose the number of the task you want to delete:')
#         self.print_tasks(tasks=tasks, for_a_day=False)
#         choice = input()
#         specific_row = tasks[int(choice) - 1]  # in case rows is not empty
#         self.session.delete(specific_row)
#         self.session.commit()
# 
#     def missed_tasks(self) -> None:
#         """
#         acquires all the records where deadline is missed in the database
#         """
#         tasks = self.session.query(Task).filter(Task.deadline < datetime.today().date()).order_by(Task.deadline).all()
#         print("Missed tasks:")
#         self.print_tasks(tasks=tasks, for_a_day=False)
# 
#     def main(self) -> None:
#         """
#         continuously runs the program
# 
#         lambda: None defines a function that does nothing, as such,
#         if wrong input was entered, it would simply go to the next iteration of the while loop
#         if choice != '0' represents the exit input, then the linebreak is replaced by a "Bye!"
#         """
#         while self.running:
#             choice = input(self.prompt)
#             self.choices.get(choice, None)()
# 
# 
# ToDoList('todo')
