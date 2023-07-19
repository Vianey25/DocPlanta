from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_mail import Mail, Message
import random
from flask_mysqldb import MySQL
from config import config
import bcrypt

app = Flask(__name__)
db = MySQL(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = '1720110004@utectulancingo.edu.mx'
app.config["MAIL_PASSWORD"] = 'Leon@2701'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEFAULT_SENDER"] = ("Jonathan Granillo Robledo", "1720110004@utectulancingo.edu.mx") 
mail = Mail(app)

# Función de decorador para verificar el estado de inicio de sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logeado' not in session or not session['logeado']:
            flash('Inicia sesión para acceder a esta página', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Función para generar una OTP aleatoria
def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    return render_template('auth/iniciar.html')

@app.route('/acceso-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cur.fetchone()

        if account and bcrypt.checkpw(password.encode('utf-8'), account[2].encode('utf-8')):
            session['logeado'] = True
            session['id'] = account[0]
            return render_template('auth/home.html')
        else:
            flash('Email o contraseña inválidos', 'error')
            return render_template('auth/iniciar.html')

@app.route('/home')
@login_required  # Aplicar el decorador login_required a la ruta
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
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur = db.connection.cursor()
        cur.execute('INSERT INTO user (email, password) VALUES (%s, %s)', (email, hashed_password))
        db.connection.commit()
        flash("El usuario ha sido registrado")
        return render_template('auth/registro.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cur.fetchone()

        if account:
            otp = generate_otp()
            session['reset_email'] = email
            session['reset_otp'] = otp

            msg = Message('Reset Your Password', recipients=[email])
            msg.body = f'Your OTP is: {otp}'
            mail.send(msg)

            flash('Se ha enviado un correo electrónico con OTP a su dirección de correo electrónico.', 'info')
            return redirect(url_for('verify_otp'))
        else:
            flash('Invalid email address', 'error')

    return render_template('auth/reset_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'reset_email' not in session or 'reset_otp' not in session:
        flash('OTP verification failed', 'error')
        return redirect(url_for('reset_password'))

    if request.method == 'POST' and 'otp' in request.form:
        otp = request.form['otp']

        if otp == session['reset_otp']:
            # OTP es correcto, permita que el usuario restablezca la contraseña
            session.pop('reset_otp', None)  # Eliminar la OTP de la sesión
            return redirect(url_for('change_password'))
        else:
            flash('OTP Invalido', 'error')

    return render_template('auth/verify_otp.html')

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'reset_email' not in session:
        flash('Unauthorized access', 'error')
        return redirect(url_for('reset_password'))

    if request.method == 'POST' and 'password' in request.form:
        email = session['reset_email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur = db.connection.cursor()
        cur.execute('UPDATE user SET password = %s WHERE email = %s', (hashed_password, email))
        db.connection.commit()
        flash('Restablecimiento de contraseña exitoso. Ahora puede iniciar sesión con su nueva contraseña.', 'success')
        session.pop('reset_email', None)

        return redirect(url_for('index'))

    return render_template('auth/change_password.html')

# Aplique el decorador login_required a las siguientes rutas
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
