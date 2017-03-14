import pypyodbc

#pypyodbc.win_create_mdb('D:\\database.mdb')

connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\database.mdb'

connection = pypyodbc.connect(connection_string)

SQL = 'CREATE TABLE saleout (id COUNTER PRIMARY KEY,product_name VARCHAR(25))'

connection.cursor().execute(SQL)

connection.cursor().commit()