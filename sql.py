import sqlite3

# # connect to sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""create table if not exists STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25) , SECTION VARCHAR(25) , MARKS INT);
"""

cursor.execute(table_info)

cursor.execute('''INSERT Into STUDENT values('krish','data science' , 'A',90)''')
cursor.execute('''INSERT Into STUDENT values('sudhanshu','data science' , 'B',100)''')
cursor.execute('''INSERT Into STUDENT values('darius','data science' , 'A',86)''')
cursor.execute('''INSERT Into STUDENT values('vikas','data science' , 'A',50)''')
cursor.execute('''INSERT Into STUDENT values('dipesh','data science' , 'A',35)''')

print("The inserted records are")

data=cursor.execute('''select * from STUDENT''')

for row in data:
    print(row)

connection.commit()
connection.close()


