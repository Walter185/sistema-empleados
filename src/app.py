from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='empleados'

mysql.init_app(app)

@app.route('/')
def index():
    # conn = mysql.connect()
    # cursor = conn.cursor()

    # sql = "insert into empleados (nombre, correo, foto) values ('Juan', 'juan@mail.com','fotodejuan.jpg');"
    # cursor.execute(sql)

    # conn.commit()
    return render_template('empleados/index.html')

@app.route('/create')
def create():
    return render_template('/empleados/create.html')

@app.route('/store', methods=['POST'])
def store():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, _foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

if __name__=='__main__':
    app.run(debug=True)
