import re
import requests
from flask import (Flask,
                    render_template,
                    request,
                    redirect,
                    session,
                    json,
                    jsonify)
from flask.helpers import url_for
import sqlite3
import time
from datetime import datetime

from operator import itemgetter

def today_date():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

app = Flask(__name__)

app.secret_key = 'super secret key'

admin_username, admin_password, admin_credentials = 'admin', 'admin', 'admin'
accounts = {'admin': {'password': 'admin', 'credentials': 'doctor'},
            'patient': {'password': 'patient', 'credentials': 'patient'},
            'doctor': {'password': 'doctor', 'credentials': 'doctor'}}


@app.route('/', methods=['GET', 'POST'])
def main():
    session.clear()
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        response = requests.post("http://localhost:5000/login", json = {'username': username,
                                                                        'password': password})
        if response.json()['status'] == 'ok':
            session['credentials'] = response.json()['credential']
            session['id'] = response.json()['id']
            session['username'] = username
            return redirect(url_for('start', username = username))                  
        else:
            pass
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        username = request.json['username']
        password_from_user = request.json['password']
        if username == 'admin' and password_from_user == 'admin':
            return jsonify({'status': 'ok', 
                    'credential': 'doctor'})
        conn = sqlite3.connect('databases/database.db')
        c = conn.cursor()  
        password_from_db = c.execute(f'SELECT password FROM persons WHERE email = \'{username}\'')
        for password_elem in password_from_db.fetchone():
            if password_elem == password_from_user:
                credentials_for_user = c.execute(f'SELECT credentials, id FROM persons WHERE email = \'{username}\'')
                for credential_elem in credentials_for_user:
                    conn.close()             
                    return jsonify({'status': 'ok', 
                                    'credential': credential_elem[0],
                                    'id': credential_elem[1]})
            else:
                conn.close() 
                return jsonify({'status': 'nok'})
    except:
        return jsonify({'status': 'nok'})


@app.route('/start')
def start():
    if not session['username']:
        return redirect(url_for('main'))
    credentials = session['credentials']
    username = session['username']
    if credentials == 'patient':
        return render_template('patient/start.html', username = username, credentials = credentials)
    elif credentials == 'doctor':
      return render_template('doctor/start.html', username = username, credentials = credentials)
    else:
        return redirect(url_for('main'))

@app.route('/office', methods=['POST', 'GET'])
def office():
    list_office = []
    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    office = c.execute(f'SELECT * FROM office')
    for row in office.fetchall():
        list_office.append(row)
    print(list_office)

    if request.method == "POST":
        name = request.form['name']
        city = request.form['city']
        street = request.form['street']
        street_number = request.form['street_number']
        phone_number = request.form['phone_number']
        email = request.form['email']
        conn = sqlite3.connect('databases/database.db')
        c = conn.cursor()
        c.execute(f'DELETE FROM office')
        conn.commit()
        c.execute(f'INSERT INTO office VALUES (\'{name}\', \'{city}\', \'{street}\',\'{street_number}\', \'{phone_number}\', \'{email}\')')
        conn.commit()
        conn.close()
    return render_template('doctor/office.html', username=session['username'], list_office=list_office[0])
        

@app.route('/add_patients', methods=['POST', 'GET'])
def add_patients():
    if session['username'] and session['credentials'] != 'doctor':
        return redirect(url_for('main'))
    
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        pesel = request.form['pesel']
        city = request.form['city']
        street = request.form['street']
        phone_number = request.form['phone_number']
        credential = 'patient'
        country = request.form['country']
        email = request.form['email']
        street_number = request.form['street_number']
        

        conn = sqlite3.connect('databases/database.db')
        c = conn.cursor()
        c.execute(f'INSERT INTO persons (name, surname, pesel, city, street, street_number, phone_number, credentials, country, email, pesel) VALUES (\'{name}\', \'{surname}\', {pesel}, \'{city}\', \'{street}\',\'{street_number}\', \'{phone_number}\', \'{credential}\', \'{country}\', \'{email}\', \'{pesel}\')')
        conn.commit()
        conn.close()

    return render_template('doctor/add_patients.html', username = session['username'])

@app.route('/add_doctors', methods=['POST', 'GET'])
def add_doctors():
    if session['username'] and session['credentials'] != 'doctor':
        return redirect(url_for('main'))
    
    list = []
    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    user_list = c.execute(f'SELECT name, surname, phone_number, email FROM persons WHERE credentials=\'doctor\'')
    for row in user_list.fetchall():
        list.append(row)

    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        phone_number = request.form['phone_number']
        credential = 'doctor'
        email = request.form['email']

        conn = sqlite3.connect('databases/database.db')
        c = conn.cursor()
        # c.execute(f'INSERT INTO doctors VALUES (\'{name}\', \'{surname}\', \'{phone_number}\', \'{credential}\', \'{email}\', \'{name}\')')
        c.execute(f'INSERT INTO persons VALUES (\'{name}\', \'{surname}\', \'\', \'\', \'\',\'\', \'{phone_number}\', \'{credential}\', \'\', \'{email}\', \'{name}\')')

        conn.commit()
        conn.close()

    return render_template('doctor/add_doctors.html', username = session['username'], list=list)


@app.route('/patients_list', methods=['POST', 'GET'])
def patients_list():
    list = []
    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    user_list = c.execute(f'SELECT id, name, surname, pesel, city, street, street_number, phone_number FROM persons WHERE credentials=\'patient\'')
    for row in user_list.fetchall():
        list.append(row)
    return render_template('doctor/patients_list.html', username = session['username'], list=list)

@app.route('/patient_info/<patient_id>', methods=['POST', 'GET'])
def patient_info(patient_id):
    patient_info = []
    tooth_info = []
    tooth_info2 = []
    teethd = [['ld8', 'ld7', 'ld6', 'ld5', 'ld4', 'ld3', 'ld2', 'ld1'], ['pd1', 'pd2', 'pd3', 'pd4', 'pd5', 'pd6', 'pd7', 'pd8']]
    teethg = [['lg8', 'lg7', 'lg6', 'lg5', 'lg4', 'lg3', 'lg2', 'lg1'], ['pg1', 'pg2', 'pg3', 'pg4', 'pg5', 'pg6', 'pg7', 'pg8']]


    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    teeth = c.execute(f'SELECT tooth, status FROM teeth WHERE patient_id = "{patient_id}"')
    if not teeth.fetchall():
        for tooth in teethd:
            for elem in tooth:
                c.execute(f'INSERT INTO teeth VALUES ({patient_id}, \'{elem}\', 2, \'\')')
        
        for tooth in teethg:
            for elem in tooth:
                c.execute(f'INSERT INTO teeth VALUES ({patient_id}, \'{elem}\', 2, \'\')')
        conn.commit()

    patient = c.execute(f'SELECT * FROM persons WHERE id = "{patient_id}"')
    for row in patient.fetchall():
        patient_info.append(row)
    

    teeth = c.execute(f'SELECT tooth, status, tooth_info FROM teeth WHERE patient_id = "{patient_id}"')
    teeth_dict = {}
    tooth_info2 = {}
    for tooth in teeth.fetchall():
        teeth_dict[tooth[0]] = tooth[1]
        
        if tooth[1] != 2:
            tooth_info2[tooth[0]] = tooth[2]
            # tooth_info2.append(tooth[0])

    if request.method == "POST":

        if request.form["submit_button"] == "submit_teeth_txt":
            for tooth_txt in request.form:
                if request.form[tooth_txt] == "submit_teeth_txt":
                    continue
                c.execute(f"UPDATE teeth SET tooth_info = '{request.form[tooth_txt]}' WHERE patient_id = {patient_id} AND tooth = '{tooth_txt}'")
            conn.commit()
            return redirect(url_for('patient_info', patient_id = patient_id))
        
        if request.form["submit_button"] == "submit_teeth_status":
            for tooth_info in request.form:
                if request.form[tooth_info] == "submit_teeth_status":
                    continue
                c.execute(f"UPDATE teeth SET status = '{request.form[tooth_info]}' WHERE patient_id = {patient_id} AND tooth = '{tooth_info}'")   
            conn.commit()
            return redirect(url_for('patient_info', patient_id = patient_id))
            # conn.close()

    return render_template('doctor/patient_info.html', patient_info=patient_info[0], teethg = teethg, teethd = teethd, teeth_dict = teeth_dict, tooth_info2=tooth_info2, patient_id=patient_id)
    

@app.route('/user_list', methods = ['GET', 'POST'])
def user_list():
    try:
        list = {}
        i = 1
        conn = sqlite3.connect('databases/database.db')
        c = conn.cursor()
        user_list = c.execute(f'SELECT name, surname, pesel, city, street, street_number, phone_number FROM persons')
        for row in user_list.fetchall():
            list[i] = row
            i += 1
        return jsonify({'status': 'ok', 'list': list})
    except:
        return jsonify({'status': 'nok'})

@app.route('/my_profile', methods = ['GET', 'POST'])
def my_profile():
    person_info = []
    username = session['username']
    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    person = c.execute(f'SELECT * FROM persons WHERE email=\'{username}\'')
    for row in person.fetchall():
        person_info.append(row)
    if request.method=='POST':
        name = request.form['name']
        surname = request.form['surname']
        phone_number = request.form['phone_number']
        email = request.form['email']
        print('trololololo')
        c.execute(f"UPDATE persons SET name='{name}', surname='{surname}', phone_number='{phone_number}', email='{email}' WHERE id={session['id']}")
        conn.commit()
    return render_template('doctor/my_profile.html', username=session['username'], person_info = person_info[0])

@app.route('/list_box', methods = ['GET', 'POST'])
def list_box():
    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    messages = c.execute(f'''SELECT m.from_column, m.to_column, p.name, p.surname, p1.name, p1.surname, m.text, MAX(m.date), m.read_flag
						FROM messages AS m
                        LEFT JOIN persons AS p
                        ON m.from_column = p.id
						LEFT JOIN persons AS p1
                        ON m.to_column = p1.id

                        WHERE to_column = 6 OR from_column = 6
                        GROUP BY m.from_column, m.to_column''')
    messages_list = []
    
    # print(messages.fetchall())
    for message in messages:
        helped_list = []
        for elem in message:
            helped_list.append(elem)
        messages_list.append(helped_list)

    while True:
        try:
            for i in range(len(messages_list)):
                for j in range(len(messages_list)):
                    if messages_list[i][0] == messages_list[j][1] and messages_list[i][1] == messages_list[j][0]:
                        if time.strptime(messages_list[i][7], "%Y-%m-%d %H:%M:%S") > time.strptime(messages_list[j][7], "%Y-%m-%d %H:%M:%S"):
                            print(messages_list[i], messages_list[j])
                            # if messages_list[i][0] == session['id']:
                            #     messages_list[i][2] = messages_list[j][2]
                            #     messages_list[i][3] = messages_list[j][3]
                            messages_list.remove(messages_list[j])
                        else:
                            # if messages_list[j][0] == session['id']:
                            #     messages_list[j][2] = messages_list[i][2]
                            #     messages_list[j][3] = messages_list[i][3]
                            messages_list.remove(messages_list[i])
        except:
            continue
        break
    messages_list = sorted(messages_list, key=itemgetter(5), reverse=True)
    # for messages in messages_list:
    #     if messages[0] == session['id']:
    #         messages[0] = messages[1]
    #         messages[1] = messages[0]
    print(messages_list)
    return render_template('doctor/list_box.html', username=session['username'], messages_list = messages_list, session_id = session['id'])

@app.route('/list_box/<id>', methods = ['GET', 'POST'])
def list_box_id(id):
    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    c.execute(f"UPDATE messages SET read_flag = 0 WHERE from_column={id} AND to_column={session['id']}")
    conn.commit()
    messages = c.execute(f'''SELECT messages.from_column, messages.to_column, persons.name, persons.surname, messages.text, messages.date, read_flag FROM messages
                        LEFT JOIN persons
                        ON messages.from_column = persons.id
                        WHERE (to_column = {id} AND from_column = {session['id']}) OR (to_column = {session['id']} AND from_column = {id})
                        ''')
    messages_list = []
    for message in messages:
        helped_list = []
        for elem in message:
            helped_list.append(elem)
        messages_list.append(helped_list)
    messages_list = sorted(messages_list, key=itemgetter(5), reverse=True)
    messages_with = c.execute(f"SELECT name, surname FROM persons WHERE id = {id}")
    messages_with = messages_with.fetchall()

    if request.method == 'POST':
        messages_to_send = request.form['message_to_send']
        print(messages_to_send, session['id'], id, today_date)
        c.execute(f"INSERT INTO messages (from_column, to_column, date, text, read_flag) VALUES ({session['id']}, {id}, '{today_date()}', '{messages_to_send}', 1)")
        conn.commit()
        return redirect(url_for('list_box_id', id = id))
    return render_template('doctor/list_box_id.html', messages_list = messages_list, id = session['id'], messages_with = messages_with)