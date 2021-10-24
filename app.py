import re
import requests
from flask import (Flask,
                    render_template,
                    request,
                    redirect,
                    session,
                    request,
                    json,
                    jsonify)
from flask.helpers import url_for

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
        session['username'] = username
        print('hehehe', accounts[username]['password'])
        if password == accounts[username]['password']:
            session['credentials'] = accounts[username]['credentials']

            return redirect(url_for('start', username = username))
        else:
            pass
    return render_template('login.html')


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


@app.route('/add_patients_doctors', methods=['POST', 'GET'])
def add_patients_doctors():
    if session['username'] and session['credentials'] != 'doctor':
        return redirect(url_for('main'))
    
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        pesel = request.form['pesel']
        city = request.form['city']
        street = request.form['street']
        phone_number = request.form['phone_number']
        response = requests.post("http://localhost:5000/add_user", json = {"name": name,
                                                    "surname": surname,
                                                    "pesel": pesel,
                                                    "city": city,
                                                    "street": street,
                                                    "phone_number": phone_number})
        if response.json()['status'] == 'ok':
            pass

    return render_template('doctor/add_patients_doctors.html', username = session['username'])

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    try:
        name = request.json['name']
        surname = request.json['surname']
        pesel = request.json['pesel']
        city = request.json['city']
        street = request.json['street']
        phone_number = request.json['phone_number']
        print(request.json)
        file = open('text.txt', 'a')
        file.write(str(request.json))
        return jsonify({'status': 'ok'})
    except:
        return jsonify({'status': 'nok'})

@app.route('/patients_list', methods=['POST', 'GET'])
def patients_list():
    return render_template('doctor/patients_list.html', username = session['username'])