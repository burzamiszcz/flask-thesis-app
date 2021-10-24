from flask import (Flask,
                    render_template,
                    request,
                    redirect)
from flask.helpers import url_for

app = Flask(__name__)


admin_username, admin_password = 'admin', 'admin'
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        if username == admin_username and password == admin_password:
            print(username)
            return redirect(url_for('start', username = username))
        else:
            pass
    return render_template('login.html')

@app.route('/<username>')
def start(username):
    username=username
    return render_template('start.html')