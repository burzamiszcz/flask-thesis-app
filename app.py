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
                credentials_for_user = c.execute(f'SELECT credentials FROM persons WHERE email = \'{username}\'')
                for credential_elem in credentials_for_user.fetchone():
                    conn.close()             
                    return jsonify({'status': 'ok', 
                                    'credential': credential_elem})
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
    teethd = [['ld8', 'ld7', 'ld6', 'ld5', 'ld4', 'ld3', 'ld2', 'ld1'], ['pd1', 'pd2', 'pd3', 'pd4', 'pd5', 'pd6', 'pd7', 'pd8']]
    teethg = [['lg8', 'lg7', 'lg6', 'lg5', 'lg4', 'lg3', 'lg2', 'lg1'], ['pg1', 'pg2', 'pg3', 'pg4', 'pg5', 'pg6', 'pg7', 'pg8']]


    conn = sqlite3.connect('databases/database.db')
    c = conn.cursor()
    teeth = c.execute(f'SELECT tooth, status FROM teeth WHERE patient_id = "{patient_id}"')
    if not teeth.fetchall():
        for tooth in teethd:
            for elem in tooth:
                c.execute(f'INSERT INTO teeth VALUES ({patient_id}, \'{elem}\', 2)')
        
        for tooth in teethg:
            for elem in tooth:
                c.execute(f'INSERT INTO teeth VALUES ({patient_id}, \'{elem}\', 2)')
        conn.commit()

    patient = c.execute(f'SELECT * FROM persons WHERE id = "{patient_id}"')
    for row in patient.fetchall():
        patient_info.append(row)

    teeth = c.execute(f'SELECT tooth, status FROM teeth WHERE patient_id = "{patient_id}"')
    teeth_dict = {}
    for tooth in teeth.fetchall():
        teeth_dict[tooth[0]] = tooth[1]
    print(teeth_dict)
    # for tooth in teeth:
    #     tooth_info.append(tooth)
    # print(tooth_info)
    # c.execute(f'INSERT INTO teeth VALUES (\'{patient_id}\', ')

    if request.method == "POST":
        c.execute(f'DELETE FROM teeth WHERE patient_id = {patient_id}')
        conn.commit()

        for tooth_info in request.form:
            print(patient_id, tooth_info, request.form[tooth_info])
            c.execute(f'INSERT INTO teeth VALUES ({patient_id}, \'{tooth_info}\', {request.form[tooth_info]})')   
        conn.commit()
        return redirect(url_for('patient_info', patient_id = patient_id))
        # conn.close()

    return render_template('doctor/patient_info.html', patient_info=patient_info[0], teethg = teethg, teethd = teethd, teeth_dict = teeth_dict)
    

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

    # if request.method == "POST":
    #     name = request.form['name']
    #     city = request.form['city']
    #     street = request.form['street']
    #     street_number = request.form['street_number']
    #     phone_number = request.form['phone_number']
    #     email = request.form['email']
    #     conn = sqlite3.connect('databases/database.db')
    #     c = conn.cursor()
    #     c.execute(f'DELETE FROM office')
    #     conn.commit()
    #     c.execute(f'INSERT INTO office VALUES (\'{name}\', \'{city}\', \'{street}\',\'{street_number}\', \'{phone_number}\', \'{email}\')')
    #     conn.commit()
    #     conn.close()
    return render_template('doctor/my_profile.html', username=session['username'], person_info = person_info[0])


