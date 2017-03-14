import pypyodbc
import sys, os, time
#pypyodbc.win_create_mdb('D:\\database.mdb')

connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\testing.mdb'

connection = pypyodbc.connect(connection_string)
cursor = connection.cursor()

SQL = 'select * from page'
start_time = time.time()

fields = cursor.execute(SQL)

#connection.cursor().commit()

end_time = time.time()
#for i in connection.cursor().description:
print cursor.description
for i in fields:
    print i

print end_time-start_time

SQL = 'select * from tab'
start_time = time.time()

fields = cursor.execute(SQL)

#connection.cursor().commit()

end_time = time.time()
#for i in connection.cursor().description:
print cursor.description
for i in fields:
    print i

print end_time-start_time

SQL = 'select * from filter'
start_time = time.time()

fields = cursor.execute(SQL)

#connection.cursor().commit()

end_time = time.time()
#for i in connection.cursor().description:
print cursor.description
for i in fields:
    print i

print end_time-start_time

SQL = 'select * from registerfiltermask'
start_time = time.time()

fields = cursor.execute(SQL)

#connection.cursor().commit()

end_time = time.time()
#for i in connection.cursor().description:
print cursor.description
for i in fields:
    print i

print end_time-start_time

SQL = 'select * from register'
start_time = time.time()

fields = cursor.execute(SQL)

#connection.cursor().commit()

end_time = time.time()
#for i in connection.cursor().description:
print cursor.description
# for i in fields:
#     print i

print end_time-start_time

SQL = 'select * from page order by pagetype'
start_time = time.time()

fields = cursor.execute(SQL)

#connection.cursor().commit()

end_time = time.time()
#for i in connection.cursor().description:
print cursor.description
for i in fields:
    print i

print end_time-start_time