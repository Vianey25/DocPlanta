from flask import Flask , render_template

from config import config

app=Flask(__name__)
  
@app.route('/')
def index():
    return render_template('auth/iniciar.html')

@app.route('/registro')
def register():        
    return render_template('auth/registro.html')


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=5001)