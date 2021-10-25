import sqlite3

conn = sqlite3.connect(r'C:\Users\BUH8TW\Desktop\thesis\thesis-application\databases\database.db')
c = conn.cursor()
# Utwórz tabelę
# c.execute('DROP TABLE persons')

c.execute('''CREATE TABLE persons
             (name TEXT,surname TEXT, pesel INTEGER, city TEXT, street TEXT,  phone_number TEXT, credentials TEXT, password TEXT)''')
conn.commit()
conn.close()