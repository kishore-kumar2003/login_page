from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'kishorekumar'


db = pymysql.connect(
    host="localhost",
    user="root",
    password="kishorekumar",
    database="project1"
)
cursor = db.cursor()


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            return 'Passwords do not match'

        cursor.execute('''CREATE TABLE IF NOT EXISTS app_user (
            name VARCHAR(50) NOT NULL,
            email VARCHAR(60) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        )''')
        cursor.execute('INSERT INTO app_user (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
        db.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute('SELECT * FROM app_user WHERE email = %s', (email,))
        user = cursor.fetchone()  

        if user:
            if user[2] == password:  
                session['username'] = user[0] 
                return redirect(url_for('home'))
            else:
                return 'Incorrect password. Please try again.'
        else:
            return 'User does not exist. Please try again.'

    return render_template('login.html')


@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
