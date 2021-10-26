import sqlite3

conn = sqlite3.connect('.\\databases\\database.db')
c = conn.cursor()
# Utwórz tabelę
# c.execute('DROP TABLE persons')

def patients():
    c.execute('''CREATE TABLE patients
                (name TEXT,surname TEXT, pesel INTEGER, city TEXT, street TEXT, street_number TEXT,  phone_number TEXT, credentials TEXT, country TEXT, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def doctors():
    c.execute('''CREATE TABLE doctors
                (name TEXT, surname TEXT, phone_number TEXT, credentials TEXT, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def office():
    c.execute('''CREATE TABLE office
                (name TEXT, city TEXT, street TEXT, street_number TEXT,  phone_number TEXT, email TEXT)''')
    conn.commit()
    conn.close()

doctors()