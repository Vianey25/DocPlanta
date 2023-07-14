from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, Response
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

db = MySQL(app)

# Decorator function to check login status
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logeado' not in session or not session['logeado']:
            flash('Inicia sesión para acceder a esta página', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('auth/iniciar.html')

@app.route('/acceso-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        account = cur.fetchone()

        if account:
            session['logeado'] = True
            session['id'] = account[0]
            return render_template('auth/home.html')
        else:
            flash('Email o contraseña inválidos', 'error')
            return render_template('auth/iniciar.html')

@app.route('/home')
@login_required  # Apply login_required decorator to the route
def home():
    return render_template('auth/home.html')

@app.route('/registro')
def register1():
    return render_template('auth/registro.html')

@app.route('/accion-registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO user (email, password) VALUES (%s, %s)', (email, password))
        db.connection.commit()
        flash("El usuario ha sido registrado")
        return render_template('auth/registro.html')

# Apply login_required decorator to the following routes
@app.route('/plantas')
@login_required
def plantas():
    return render_template('auth/plantas.html')

@app.route('/enfermedades')
@login_required
def enfermedades():
    return render_template('auth/enfermedades.html')

@app.route('/invernadero')
@login_required
def invernadero():
    return render_template('auth/invernadero.html')

@app.route('/temperatura-humedad')
@login_required
def temperatura_humedad():
    return render_template('auth/temperatura_humedad.html')

@app.route('/sensores')
@login_required
def sensores():
    return render_template('auth/sensores.html')

@app.route('/cursos')
@login_required
def cursos():
    return render_template('auth/cursos.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=5001)
