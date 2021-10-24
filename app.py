from flask import (Flask,
                    render_template,
                    request,
                    redirect,
                    session)
from flask.helpers import url_for

app = Flask(__name__)

app.secret_key = 'super secret key'

admin_username, admin_password, credentials = 'admin', 'admin', 'admin'

@app.route('/', methods=['GET', 'POST'])
def main():
    session.clear()
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        session['username'] = username
        if username == admin_username and password == admin_password:
            print(username)
            return redirect(url_for('start', username = username))
        else:
            pass
    return render_template('login.html')

@app.route('/start/<username>')
def start(username):
    if session['username'] != username:
        return redirect(url_for('main'))

    username = session['username']
    return render_template('start.html', username = username)