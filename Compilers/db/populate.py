import db_conn as db

sql_file = open('populate2.sql')

sql = sql_file.read()

conn = db.getConnection('compilers.db')
conn.executescript(sql)

conn.commit()
conn.close()