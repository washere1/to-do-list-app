#!/usr/bin/python3

import cgitb
cgitb.enable()

print("Content-type:text/html")
print()

import sqlite3
from helper_functions import show_data, get_input, todo_app, tasks_html

connection = sqlite3.connect('app.db')

sql = connection.cursor()

############ E X E R C I S E S ################
#
#  Exercise 6: Create a table for todo list.
#
#  Exercise 7: Show the todo list app on login.
#
#  Exercise 8: Create a function to add tasks in our todolist table.
#
#  Exercise 9: Send request to add new tasks from todolist.html.
#
#  Bonus Exercise: Update the task status when clicked on it.
####################################################

sql.execute('''
create table if not exists users (
    userId integer primary key autoincrement,
    firstname Text,
    lastname Text,
    email Text,
    password Text
)''')

sql.execute('''
create table if not exists todolist (
    "userId" integer,
    "taskId" integer primary key autoincrement,
    "task" Text,
    "status" Text
)''')

def signup(first_name, last_name, email, password):
    data = sql.execute('select * from users where email = ?', [email])
    total_rows = len(data.fetchall())
    if total_rows > 0:
        print("<script>alert('There is already an account with same email id'); window.location.reload();</script>")
    else:
        sql.execute('insert into users (firstname, lastname, email, password) values (?, ?, ?, ?)', [first_name, last_name, email, password])
        connection.commit()
        login(email, password)

def login(email, password):
    data = sql.execute('''select * from users 
    left outer join todolist using(userId)
    where email = ? AND password = ?''', [email, password])
    rows = data.fetchall()
    row_count = len(rows)
    if(row_count > 0):
        todo_app(rows)
    else:
        print("<script>alert('Incorrect username or password'); window.location.reload();</script>")

        
def add_task(userId, task):
    sql.execute('''insert into todolist
    (userId, task, status) values (?,?,"incomplete")''', [userId, task])
    connection.commit()
    show_tasks(userId)
    
def show_tasks(userId):
    data = sql.execute('''select * from todolist
    where userId = ?''', [userId])
    tasks_html(data)

user_input = get_input()

if user_input:
    mode = user_input['mode']
    if mode == 'signup':
        signup(user_input['firstname'], user_input['lastname'], user_input['email'], user_input['password'])
    elif mode == 'login':
        login(user_input['email'], user_input['password'])
    elif mode == 'add':
        add_task(user_input['userId'], user_input['task'])
else:
    print("No input given by user")
