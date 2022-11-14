from colorama import Cursor
from flask import Flask
from flask import render_template,request,redirect #solicitar la informacion
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


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


#crear nuevo empleado
@app.route('/create')
def create():
    
    return render_template('empleados/create.html')









if __name__== '__main__':

    app.run(host="0.0.0.0")  ##port=4000