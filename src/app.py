from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        return render_template('auth/iniciar.html')
    else:
        return render_template('auth/iniciar.html')

@app.route('/home')
def register1():
    return render_template('auth/home.html')


@app.route('/registro')
def register():
    return render_template('auth/registro.html')


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
