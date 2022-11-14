from colorama import Cursor
from flask import Flask
from flask import render_template,request,redirect #solicitar la informacion
from flaskext.mysql import MySQL
from flask import send_from_directory # mostrar elementos en un directorio

from datetime import datetime
import os  # importar modulo de sistema operativo


#from zmq import ContextOption
# crear la aplicacion
app= Flask(__name__)  

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

# Referencia con valor de carpeta
Carpeta=os.path.join('uploads')
app.config['Carpeta']=Carpeta   # crean referencia a una variable para guardar la ruta como un valor de carpeta

#Solicitar url y mostrar imagenes
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['Carpeta'],nombreFoto)


#Insertar empleado
@app.route('/')
def index():

    sql="SELECT * FROM `empleados`;"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()

    return render_template ('empleados/index.html', empleados=empleados ) #enviar los datos a tavez de la variable


# Eliminar empleado
@app.route('/destroy/<int:id>')
def destroy(id):
    pass
    conn= mysql.connect()
    cursor= conn.cursor()
    
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id))
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['Carpeta'],fila[0][0]))
    
    cursor.execute("DELETE FROM Empleados WHERE id=%s",(id)) # se asigna la instruccion SQL directa
    conn.commit()
    return redirect('/')

# Editar empleados para ser Actualizado
@app.route('/edit/<int:id>')
def edit(id):

    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    print(empleados)
    return render_template ('empleados/edit.html', empleados=empleados) 
    
# Metodo actualizar empleados
@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtnombre']
    _correo=request.form['txtcorreo']
    _foto=request.files['txtfoto']
    id=request.form['txtID']

    sql="UPDATE `empleados` SET `nombre`=%s, `correo`=%s WHERE `id`=%s ;"

    datos=(_nombre,_correo,id)

    conn= mysql.connect()
    cursor= conn.cursor()

    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

     #si el  campo no esta vacio concatenamos dato del  tiempo + nombre d ela fotografia y no sobreescribir a un foto anterior 
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", (id))
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['Carpeta'],fila[0][0]))
        cursor.execute("UPDATE `empleados` SET `foto`=%s WHERE `id`=%s", (nuevoNombreFoto,id))
        conn.commit()

    cursor.execute(sql,datos)  # asignar nuevo nombre a la imagen
    conn.commit()
    return redirect('/')
    

#crear nuevo empleado
@app.route('/create')
def create():
    
    return render_template('empleados/create.html')

#crear un nuevo empleado desde formulario create html
@app.route('/store', methods=['POST'])
def storage():

    _nombre=request.form['txtnombre']
    _correo=request.form['txtcorreo']
    _foto=request.files['txtfoto']

    #al subir la fotografia se captura el  dato del  tiempo
    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    #si el  campo no esta vacio concatenamos dato del  tiempo + nombre d ela fotografia y no sobreescribir a un foto anterior 
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    
    sql="INSERT INTO `empleados` (`Id`, `Nombre`, `Correo`, `Foto`) VALUES (NULL, %s, %s, %s);"

    datos=(_nombre,_correo,_foto.filename)

    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')
    #return render_template('empleados/create.html')

    

if __name__== '__main__':

    app.run(host="0.0.0.0")

