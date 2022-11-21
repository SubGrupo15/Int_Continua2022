from datetime import datetime
from colorama import Cursor
from flask import Flask, redirect, render_template, request, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory


# crear la aplicacion
app = Flask(__name__)
app.secret_key="Mensaje"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

# Referencia con valor de carpeta # crean referencia a una variable para guardar la ruta como un valor de carpeta
CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA

# Solicitar url y mostrar imagenes
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)


# Insertar empleado
@app.route('/')
def index():

    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit()

    # enviar los datos a tavez de la variable
    return render_template('empleados/index.html', empleados=empleados)


# Eliminar empleado
@app.route('/destroy/<int:id>')
def destroy(id):
    #pass
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Empleados WHERE id=%s", (id))
    conn.commit()
    return redirect('/')
    
    """ # Nov 20
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id))
    fila = cursor.fetchall() """

    """ os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    #se asigna la instruccion SQL directa """

    

# Editar empleados para ser Actualizado


@app.route('/edit/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados = cursor.fetchall()
    conn.commit()
    # print(empleados)

    return render_template('empleados/edit.html', empleados=empleados)

# Metodo actualizar empleados

@app.route('/update', methods=['POST']) 
def update():

    _nombre = request.form['txtnombre']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto']
    id = request.form['txtID']

    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s ;"

    datos = (_nombre, _correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)  # asignar nuevo nombre a la imagen
    conn.commit() 

    return redirect('/')
     
    """ #Nov 20 en validacion o  para comentar si  genera error
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    # si el  campo no esta vacio concatenamos dato del  tiempo + nombre d ela fotografia y no sobreescribir a un foto anterior
    if _foto.filename != '':

        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

        #buscar como se llama la foto
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
        fila = cursor.fetchall()

        # PermissionError: [WinError 5] Acceso denegado: 'uploads\\'
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE `id`=%s", (nuevoNombreFoto,id))
        conn.commit()


 """
    
    
       


# crear nuevo empleado
@app.route('/create')
def create():

    return render_template('empleados/create.html')

# crear un nuevo empleado desde formulario create html


@app.route('/store', methods=['POST'])
def storage():

    _nombre = request.form['txtnombre']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto']



    # al subir la fotografia se captura el  dato del  tiempo
    if _nombre=='' or _correo=='' or _foto=='':
        flash('Recuerda llenar los datos de los Campos')
        return redirect (url_for('create'))

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    # si el  campo no esta vacio concatenamos dato del  tiempo + nombre d ela fotografia y no sobreescribir a un foto anterior
    
    if _foto.filename != '':
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql = "INSERT INTO `empleados` (`Id`, `Nombre`, `Correo`, `Foto`) VALUES (NULL, %s, %s, %s);"

    datos = (_nombre, _correo, _foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')
    # return render_template('empleados/create.html')


if __name__ == '__main__':

    app.run(host="0.0.0.0")
