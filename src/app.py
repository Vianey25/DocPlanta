from flask import Flask, render_template, request, redirect, url_for, jsonify,flash, send_file, session, make_response
from flask_mysqldb import MySQL
from config import config
import json
import matplotlib.pyplot as plt
from io import BytesIO
from io import BytesIO
from flask import render_template, make_response
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import PageBreak
from flask import current_app
from datetime import datetime
import base64


from models.modeluser import ModelUser

from models.entities.user import User

#from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='/static')



db = MySQL(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = User(0,request.form['email'],request.form['password'])
        logged_user = ModelUser.login(db,email)
        if logged_user != None :
            if logged_user.password:
                return render_template('auth/home.html')
            else:
                flash("contraseña no valida --")
        else:
            flash("usuario no encontrado")
        return render_template('auth/iniciar.html')
    else:
        return render_template('auth/iniciar.html')

@app.route('/home')
def register1():
    return render_template('auth/home.html')

@app.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO user (email, password) VALUES (%s, %s)', (email, password))
        db.connection.commit()
        flash("añadido")
        return redirect(url_for('register'))
    return render_template('auth/registro.html')


def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#paginacion de tablas


def get_paginated_records(page, per_page, search_query=''):
    offset = (page - 1) * per_page
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM plantas LIMIT %s OFFSET %s', (per_page, offset))
    
    if search_query:
        cur.execute('SELECT * FROM plantas WHERE nombre_planta LIKE %s LIMIT %s OFFSET %s', (f'%{search_query}%', per_page, offset))
    else:
        cur.execute('SELECT * FROM plantas LIMIT %s OFFSET %s', (per_page, offset))
        
    return cur.fetchall()

def get_paginated_records1(page, per_page):
    offset = (page - 1) * per_page
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM enfermedades LIMIT %s OFFSET %s', (per_page, offset))
    return cur.fetchall()


def get_paginated_records2(page, per_page):
    offset = (page - 1) * per_page
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM invernaderos LIMIT %s OFFSET %s', (per_page, offset))
    return cur.fetchall()

@app.route('/plantas', methods=['GET', 'POST'])
def plantas():
    per_page = 5
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')

    plants_data = get_paginated_records(page, per_page)
    
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM plantas')
    plants_data = cur.fetchall()
   
    if request.method == 'POST':
        nombre_planta = request.form['nombre_planta']
        descripcion_planta = request.form['descripcion_planta']

        cur.execute('INSERT INTO plantas (nombre_planta, descripcion_planta) VALUES (%s, %s)', (nombre_planta, descripcion_planta))
        db.connection.commit()
        id = cur.lastrowid
        return redirect(url_for('plantas', id=id, nombre_planta=nombre_planta))

    return render_template('auth/plantas.html', plants_data=plants_data)

@app.route('/plantas/delete/<int:id>', methods=['POST'])
def delete_plant(id):
    cur = db.connection.cursor()

    cur.execute('SELECT id FROM plantas WHERE id = %s', (id,))
    deleted_id = cur.fetchone()

    cur.execute('DELETE FROM plantas WHERE id = %s', (id,))
    db.connection.commit()

    if deleted_id:
        cur.execute('UPDATE plantas SET id = id - 1 WHERE id > %s', (id,))
        db.connection.commit()
        cur.execute('ALTER TABLE plantas AUTO_INCREMENT = 1')
        db.connection.commit()

    flash("Planta dada de baja")
    return redirect('/plantas')


@app.route('/plantas/update/<int:id>', methods=['GET', 'POST'])
def update_plant(id):
    if request.method == 'POST':
        nombre_planta = request.form.get('nombre_planta')
        descripcion_planta = request.form.get('descripcion_planta')
        cur = db.connection.cursor()
        cur.execute('UPDATE plantas SET nombre_planta = %s, descripcion_planta = %s WHERE id = %s',
                    (nombre_planta, descripcion_planta, id))
        db.connection.commit()
        cur.close()
        return redirect('/plantas')  
    else:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM plantas WHERE id = %s', (id,))
        plant_data = cur.fetchone()
        cur.close()
        return render_template('auth/actualizar_plantas.html', plant_data=plant_data)
    
@app.route('/enfermedades', methods=['GET', 'POST'])
def enfermedades():

    per_page = 5  # Number of records per page
    page = request.args.get('page', 1, type=int)  # Get the requested page from query parameter

    plants_data = get_paginated_records1(page, per_page)
    if request.method == 'POST':
        nombre_enfermedad = request.form['nombre_enfermedad']
        id_planta = request.form['id']
        descripcion_enfermedad = request.form['descripcion_enfermedad']
        numero_plantas = request.form['numero_plantas']
        record_data = request.form['record_data']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO enfermedades (nombre_enfermedad, id_planta, numero_plantas, descripcion_enfermedad, record_data) VALUES (%s, %s, %s, %s, %s)', (nombre_enfermedad, id_planta,numero_plantas, descripcion_enfermedad, record_data))
        enfer_data = cur.fetchall()

        db.connection.commit()
        flash("agregado")
        return redirect(url_for('enfermedades'))
    cur = db.connection.cursor()
    cur.execute('SELECT enfermedades.id, enfermedades.nombre_enfermedad, plantas.nombre_planta, enfermedades.numero_plantas, enfermedades.descripcion_enfermedad, enfermedades.record_data FROM enfermedades INNER JOIN plantas ON enfermedades.id_planta = plantas.id')
    enfer_data = cur.fetchall()

    cur.execute('SELECT id, nombre_planta FROM plantas')
    plants_data = cur.fetchall()

    return render_template('auth/enfermedades.html', enfer_data=enfer_data, plants_data=plants_data)

@app.route('/enfermedades/delete/<int:id>', methods=['POST'])
def delete_enfermedad(id):
    cur = db.connection.cursor()

    cur.execute('SELECT id FROM enfermedades WHERE id = %s', (id,))
    deleted_id = cur.fetchone()

    cur.execute('DELETE FROM enfermedades WHERE id = %s', (id,))
    db.connection.commit()

    if deleted_id:
        cur.execute('UPDATE enfermedades SET id = id - 1 WHERE id > %s', (id,))
        db.connection.commit()
        cur.execute('ALTER TABLE enfermedades AUTO_INCREMENT = 1')
        db.connection.commit()

    flash("enfermedad dada de baja")
    return redirect('/enfermedades')

@app.route('/enfermedades/update/<int:id>', methods=['GET', 'POST'])
def update_enfermedad(id):
    if request.method == 'POST':
        nombre_enfermedad = request.form['nombre_enfermedad']
        id_planta = request.form['id']
        descripcion_enfermedad = request.form['descripcion_enfermedad']
        cur = db.connection.cursor()
        cur.execute('UPDATE enfermedades SET nombre_enfermedad = %s, id_planta = %s, descripcion_enfermedad = %s WHERE id = %s',
                    (nombre_enfermedad, id_planta, descripcion_enfermedad, id))
        db.connection.commit()
        cur.close()
        return redirect('/enfermedades')  
    else:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM enfermedades WHERE id = %s', (id,))
        enfer_data = cur.fetchone()
        cur.close()

        cur = db.connection.cursor()
        cur.execute('SELECT id, nombre_planta FROM plantas')
        plants_data = cur.fetchall()

        return render_template('auth/actualizar_enfermedades.html', enfer_data=enfer_data, plants_data=plants_data)
    
@app.route('/reporte_enfer', methods=['GET', 'POST'])
def reporte_enfer():
    if request.method == 'POST':
      start_date = request.form['start_date']
      end_date = request.form['end_date']
      print("Start Date:", start_date)
      print("End Date:", end_date)
      start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
      end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
      session['start_date'] = start_date
      session['end_date'] = end_date

      cur = db.connection.cursor()
      query= "SELECT enfermedades.nombre_enfermedad, SUM(enfermedades.numero_plantas) FROM enfermedades WHERE enfermedades.record_data BETWEEN %s AND %s GROUP BY enfermedades.nombre_enfermedad"
      cur.execute(query, (start_datetime, end_datetime))
      disease_counts = cur.fetchall()

      cur = db.connection.cursor()
      query = "SELECT enfermedades.id, enfermedades.nombre_enfermedad, plantas.nombre_planta, enfermedades.numero_plantas, enfermedades.descripcion_enfermedad, enfermedades.record_data FROM enfermedades INNER JOIN plantas ON enfermedades.id_planta = plantas.id WHERE enfermedades.record_data BETWEEN %s AND %s"
      cur.execute(query, (start_datetime, end_datetime))
      enfer_data = cur.fetchall()


      graph_data = {
       'labels': [entry[0] for entry in disease_counts],  
       'data': [float(entry[1]) for entry in disease_counts]  
      }
      return render_template('auth/repor_enfermedades.html', enfer_data=enfer_data, graph_data=json.dumps(graph_data))


    return render_template('auth/repor_enfermedades.html')



@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    cur = db.connection.cursor()
    cur.execute('SELECT enfermedades.nombre_enfermedad, SUM(enfermedades.numero_plantas) FROM enfermedades GROUP BY enfermedades.nombre_enfermedad')
    disease_counts = cur.fetchall()
    graph_data = {
        'labels': [entry[0] for entry in disease_counts],
        'data': [float(entry[1]) for entry in disease_counts]
    }
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    start_date = session.get('start_date')
    end_date = session.get('end_date')

    table_data = [['Enfermedad', 'Nombre de la planta', 'Numero de plantas enfermas']]

    cur = db.connection.cursor()
    cur.execute('SELECT enfermedades.nombre_enfermedad, plantas.nombre_planta, SUM(enfermedades.numero_plantas) FROM enfermedades INNER JOIN plantas ON enfermedades.id_planta = plantas.id GROUP BY enfermedades.nombre_enfermedad, plantas.nombre_planta')
    enfermeda_planta_suma = cur.fetchall()

    cur = db.connection.cursor()
    cur.execute('SELECT plantas.nombre_planta, SUM(enfermedades.numero_plantas) FROM enfermedades INNER JOIN plantas ON enfermedades.id_planta = plantas.id GROUP BY plantas.nombre_planta')
    numero_plantas = cur.fetchall()

    
    cur = db.connection.cursor()
    cur.execute('SELECT enfermedades.nombre_enfermedad, plantas.nombre_planta, SUM(enfermedades.numero_plantas) FROM enfermedades INNER JOIN plantas ON enfermedades.id_planta = plantas.id GROUP BY enfermedades.nombre_enfermedad, plantas.nombre_planta')
    total = cur.fetchall()

    print("End Date:", numero_plantas)

    for entry in enfermeda_planta_suma:
        table_data.append([entry[0], entry[1], entry[2]])

    
    total_diseased_plants = sum(entry[2] for entry in total)
    table_data.append(['Total', '', total_diseased_plants])
    table = Table(table_data, colWidths=[200, 200, 200]) 
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),  
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),   
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),      
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),      
        ('BACKGROUND', (0, 1), (-1, -1), '#F0F0F0'), 
    ])
    

    table.setStyle(table_style)
    text_content = []
    text_content.append("La evaluación indica que de {} a {} se detectaron plantas enfermas, de las cuales se realizo un suma por cada tipo de planta:".format(start_date, end_date) )
    for entry in numero_plantas:
        nombre_planta = entry[0]
        numero_enfer_planta = entry[1]
        text_content.append("° {}: {} plantas enfermas".format(nombre_planta, numero_enfer_planta))
    text_paragraphs = '\n'.join(text_content)

    title = Paragraph("Reporte de enfermedades de {} a {}".format(start_date, end_date), styles['Title'])
    #title = Paragraph("Reporte de enfermedades", styles['Title'])
    story = [title]
    text = "Este reporte de evaluación de enfermedades de las plantas tiene como objetivo analizar las enfermedades que afectan a las plantas en [su jardín/granja/ubicación]. La evaluación se llevó a cabo durante un período de tiempo, e involucró observaciones y análisis detallados de varias especies de plantas presentes en el sitio. El informe proporciona información sobre los tipos de enfermedades observadas, sus posibles causas y las estrategias de gestión recomendadas para mitigar su impacto."
    story.append(Paragraph(text, styles['Normal']))
    story.append(Spacer(1, 15)) 
    story.append(table)
    story.append(Spacer(1, 15)) 
    story.append(Paragraph(text_paragraphs, styles['Normal']))
    doc.build(story)
    response = make_response(buffer.getvalue())

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename="reporte_enfermedades.pdf"'


    return response

@app.route('/invernadero', methods=['GET', 'POST'])
def invernadero():
    per_page = 5  
    page = request.args.get('page', 1, type=int)  

    plants_data = get_paginated_records2(page, per_page)
    if request.method == 'POST':
        nombre_invernadero = request.form['nombre_invernadero']
        id_planta = request.form['id']
        tem_max	 = float(request.form['tem_max'])
        tem_min	 = float(request.form['tem_min'])
        hum_max	 = float(request.form['hum_max'])
        hum_min	 = float(request.form['hum_min'])
        descripcion	 = request.form['descripcion']
        if hum_max > 100:
            hum_max = hum_max / 100.0
        if hum_min > 100:
            hum_min = hum_min / 100.0

        cur = db.connection.cursor()
        cur.execute('INSERT INTO invernaderos (nombre_invernadero,id_planta, tem_max, tem_min, hum_max, hum_min, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)', (nombre_invernadero,id_planta, tem_max, tem_min, hum_max, hum_min, descripcion))
        db.connection.commit()
        flash("añadido")
        return redirect(url_for('invernadero'))
    
    cur = db.connection.cursor()
    cur.execute('SELECT invernaderos.id, invernaderos.nombre_invernadero,invernaderos.id_planta, invernaderos.tem_max, invernaderos.tem_min, invernaderos.hum_max, invernaderos.hum_min, invernaderos.descripcion FROM invernaderos INNER JOIN plantas ON invernaderos.id_planta = plantas.id')
    inver_data = cur.fetchall()

    cur.execute('SELECT id, nombre_planta FROM plantas')
    plants_data = cur.fetchall()
    
    return render_template('auth/invernadero.html', inver_data=inver_data, plants_data=plants_data)

@app.route('/invernadero/delete/<int:id>', methods=['POST'])
def delete_invernadero(id):
    cur = db.connection.cursor()

    cur.execute('SELECT id FROM invernaderos WHERE id = %s', (id,))
    deleted_id = cur.fetchone()

    cur.execute('DELETE FROM invernaderos WHERE id = %s', (id,))
    db.connection.commit()

    if deleted_id:
        cur.execute('UPDATE invernaderos SET id = id - 1 WHERE id > %s', (id,))
        db.connection.commit()
        cur.execute('ALTER TABLE invernaderos AUTO_INCREMENT = 1')
        db.connection.commit()

    flash("invernadero dada de baja")
    return redirect('/invernadero')

@app.route('/invernadero/update/<int:id>', methods=['GET', 'POST'])
def update_(id):
    if request.method == 'POST':
        nombre_invernadero = request.form['nombre_invernadero']
        id_planta = request.form['id']
        tem_max	 = float(request.form['tem_max'])
        tem_min	 = float(request.form['tem_min'])
        hum_max	 = float(request.form['hum_max'])
        hum_min	 = float(request.form['hum_min'])
        descripcion	 = request.form['descripcion']
        if hum_max > 100:
            hum_max = hum_max / 100.0
        if hum_min > 100:
            hum_min = hum_min / 100.0

        cur = db.connection.cursor()
        cur.execute('UPDATE invernaderos SET nombre_invernadero = %s, id_planta = %s, tem_max = %s, tem_min = %s, hum_max = %s, hum_min =%s, descripcion = %s WHERE id = %s',
                    (nombre_invernadero, id_planta, tem_max, tem_min, hum_max, hum_min, descripcion, id))
        db.connection.commit()
        cur.close()
        return redirect('/invernadero')  
    else:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM invernaderos WHERE id = %s', (id,))
        inver_data = cur.fetchone()
        cur.close()

        cur = db.connection.cursor()
        cur.execute('SELECT id, nombre_planta FROM plantas')
        plants_data = cur.fetchall()

        return render_template('auth/actualizar_invernadero.html', inver_data=inver_data, plants_data=plants_data)


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
