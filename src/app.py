from flask import Flask, render_template, request, redirect, url_for, jsonify,flash
from flask_mysqldb import MySQL
from config import config

from models.modeluser import ModelUser

from models.entities.user import User

app = Flask(__name__)

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = User(0,request.form['email'],request.form['password'])
        logged_user = ModelUser.login(db,email)
        if logged_user != None :
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash("contraseña no valida")
        else:
            flash("usuario no encontrado")
        return render_template('auth/iniciar.html')
    else:
        return render_template('auth/iniciar.html')

@app.route('/home')
def register1():
    return render_template('auth/home.html')



@app.route('/registro', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.excecute('INSERT INTO registro (usuario,email,password) VALUES (%s,%s,%s)',(usuario,email,password))
        db.connection.commit()
        flash("añadido")
        return redirect(url_for('registro.html'))


@app.route('/plantas')
def plantas():
    return render_template('auth/plantas.html')


@app.route('/enfermedades')
def enfermedades():
    return render_template('auth/enfermedades.html')

@app.route('/invernadero')
def invernadero():
    return render_template('auth/invernadero.html')

@app.route('/temperatura-humedad')
def temperatura_humedad():
    return render_template('auth/temperatura_humedad.html')

@app.route('/sensores')
def sensores():
    return render_template('auth/sensores.html')

@app.route('/cursos')
def cursos():
    return render_template('auth/cursos.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=5001)
