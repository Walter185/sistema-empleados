from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='empleados'

UPLOADS= os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS

mysql.init_app(app)

@app.route('/fotodeusuario/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('uploads'), nombreFoto)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * from empleados;"
    cursor.execute(sql)
    empleados = cursor.fetchall()
 
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)

@app.route('/create')
def create():
    return render_template('/empleados/create.html')

@app.route('/save', methods=['POST'])
def store():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    now = datetime.now()
    print(now)
    tiempo = now.strftime("%Y%H%M%S")
    print(tiempo)

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)


    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor() 

    sql = f'SELECT foto FROM empleados WHERE id="{id}";'
    cursor.execute(sql)

    nombreFoto = cursor.fetchone()[0]

    try:
        os.remove(os.path.join(app.config['UPLOADS'],nombreFoto))
    except:
        pass

    sql = f'DELETE FROM empleados WHERE id={id}'
    cursor.execute(sql)
    conn.commit()

    return redirect('/')


@app.route('/modify/<int:id>')
def modify(id):
    sql = f'SELECT * FROM empleados WHERE id="{id}"'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleado=cursor.fetchone()
    conn.commit()
    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)

        sql = f'SELECT foto FROM empleados WHERE id="{id}"'
        cursor.execute(sql)
        conn.commit()

        nomnbreFoto = cursor.fetchone()[0]
        borrarEstaFoto = os.path.join(app.config['UPLOADS'], nomnbreFoto)
        print(borrarEstaFoto)

        try:
            os.remove(os.path.join(app.config['UPLOADS'], nomnbreFoto))
        except:
            pass

        sql = f'UPDATE empleados SET foto="{nuevoNombreFoto}" WHERE id="{id}";'
        cursor.execute(sql)
        conn.commit()


    sql = f'UPDATE empleados SET nombre="{_nombre}", correo="{_correo}" WHERE id="{id}"'
    cursor.execute(sql)
    conn.commit()

    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
