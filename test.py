#! Users/wildcard/AppData/Local/Programs/Python35/python.exe

import mysql.connector
""" MySQL database and Python """

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

conn = mysql.connector.connect(host='localhost',
                              database='webair',
                              user='root',
                              password='')
if conn.is_connected():
   print('Connected to MySQL database')
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM timetable")
   for row in iter_row(cursor, 10):
       print(row)      
   cursor.close()
conn.close()
 
 