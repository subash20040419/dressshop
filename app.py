from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!

# MySQL Config (make sure XAMPP is running)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'       # default for XAMPP
app.config['MYSQL_PASSWORD'] = ''       # leave blank unless you set one
app.config['MYSQL_DB'] = 'dress_shop'

mysql = MySQL(app)

# ---------- ROUTES ----------


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('⚠️ Email already registered!', 'danger')
        elif password != confirm_password:
            flash('❌ Passwords do not match!', 'danger')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('❌ Invalid email format!', 'danger')
        else:
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                           (name, email, password))
            mysql.connection.commit()
            flash('✅ Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('index3.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            flash('✅ Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('❌ Incorrect Email or Password!', 'danger')

    return render_template('index4.html')


@app.route('/home')
def home():
    return render_template('index.html')





@app.route('/products')
def products():
    return render_template('index2.html')

@app.route('/mens')
def mens():
    return render_template('index8.html')

@app.route('/womans')
def womans():
    return render_template('index9.html')

@app.route('/kids')
def kids():
    return render_template('index10.html')

@app.route('/contact')
def contact():
    return render_template('index6.html')

@app.route('/about')
def about():
    return render_template('index5.html')








if __name__ == '__main__':
    app.run(debug=True)
