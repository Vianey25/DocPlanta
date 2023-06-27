from flask import Flask , render_template

from config import config 

app=Flask(__name__)
  
@app.route('/')
def index():
    return render_template('auth/iniciar.html')

@app.route('/registro')
def register():        
    return render_template('auth/registro.html')

@app.route('/plantas')
def plantas():        
    return render_template('auth/plantas.html')

@app.route('/enfermedades')
def enfermedades():        
    return render_template('auth/enfermedades.html')

@app.route('/temperatura-humedad')
def temperatura_humedad():        
    return render_template('auth/temperatura-humedad.html')

@app.route('/invernaderos')
def invernaderos():        
    return render_template('invernaderos.html')

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=5001)