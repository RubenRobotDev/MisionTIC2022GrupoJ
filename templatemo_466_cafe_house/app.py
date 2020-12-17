from flask import Flask as fl
from flask import render_template, request, redirect, url_for, session, g
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from db import close_db
from db import get_db
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/sql/databaseusuario.db"

app = fl(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = os.urandom(24)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    correoelectronico = db.Column(db.String(50), unique=True)
    contraseña = db.Column(db.String(30), nullable=False)
    

#JM lo modifiqué para que buscque en la base de datos el usuario
@app.route("/",methods=["GET","POST"])
def hello():
    flash("hola")
    print("prueba de flash")
    if request.method == 'POST':
        #print('si mandó un método post')
        #necesito que se conecte a la base de datos. 
        close_db()
        db_Activa = get_db()

        #saco las variables
        user = str(request.form["user"])
        print(type(user))
        print(user)
        password = str(request.form["pass"])

        #valido que si pusiera algo en cada uno de los campos. 
        if not user: 
            error = "El usuario es requerido"
            flash(error)
            print("no hay usuario")
            return render_template('login.html')

        if not password: 
            error = "La clave es requerida"
            flash(error)
            print("no hay clave")
            return render_template('login.html')

        #hago la consulta a la base de datos para ver si el usuario existe
        query = 'SELECT * FROM usuario WHERE usuario = "' + user + '"'
        user_dataBase = db_Activa.execute(query).fetchone()
        
        if user_dataBase is None:
            error = 'Usuario o contraseña inválidos'
            print(error)
            flash(error)
            return render_template("login.html")
        else: 
            #compruebo la contraseña
            #if user_dataBase[4]== password:
            if check_password_hash(user_dataBase[4],password):
                #le saco el id verifico si es admin o usuario regular
                session.clear()
                session['user_id'] = user_dataBase[0]
                id_usuario = str(user_dataBase[0])
                # crear un query y pasarlo como parámetro
                query2 = 'SELECT * FROM Roles WHERE id_usuario = "' + id_usuario +'"'
                tipo_usuario = db_Activa.execute(query2).fetchone()
                #print(tipo_usuario[1])
                if tipo_usuario[1] == "Admin":
                    return redirect(url_for("HomeAdmin"))
                else: 
                    return redirect(url_for("HomeUser"))
            else: 
                error = 'Usuario o contraseña inválidos v2'
                print(error)
                flash(error)
                return render_template("login.html")
    else: 
        print('no mandó un método post')
        return render_template("login.html")

  

@app.route("/RecoverPassword",methods=["GET","POST"])
def RecoverPassword():
    if request.method == "POST":
        mail = request.form["email"]
        return redirect(url_for("hello"))
    else:    
        return render_template("RecoverPassword.html")

@app.route("/HomeAdmin",methods=["GET","POST"])
def HomeAdmin():
    if request.method == "POST":
        return render_template("HomeAdmin.html")
    else:    
        return render_template("HomeAdmin.html")

@app.route("/HomeUser",methods=["GET","POST"])
def HomeUser():
    if request.method == "POST":
        return render_template("HomeUser.html")
    else:   
        return render_template("HomeUser.html")

@app.route("/ManageUser",methods=["GET","POST"])
def ManageUser():
    if request.method == "POST":
        return render_template("ManageUser.html")
    else:    
        return render_template("ManageUser.html")

#crear nuevo usuario
@app.route("/NewUser",methods=["GET","POST"])
def NewUser():
    if request.method == "POST":
<<<<<<< HEAD
        User = Usuario
=======
        User=Usuario()
>>>>>>> eb1a1740ba2980f8e900f562fe87a88f375a6819
        newUserName = request.form["NewUserName"]
        newUserUser = request.form["NewUserUser"]
        newUserPassword = request.form["NewUserPassword"]
        newUserMail = request.form["NewUserMail"]

        User.nombre = newUserName
        User.usuario = newUserUser
        User.contraseña = newUserPassword
        User.correoelectronico = newUserMail

        db.session.add(User)
        db.session.commit()
        
        return "hecho"

    else:    
        return render_template("NewUser.html")


@app.route("/SearchUser",methods=["GET","POST"])
def SearchUser():
    print('Entro a search User method')

    close_db()
    db_Activa = get_db()
    
    if request.method == 'POST':
        print('Entro a POST User method')
        #search user tiene usuario que se busca
        searchUser = request.form["search"]

        #valido que no esté vacio
        if not searchUser: 
            error = "El usuario es requerido"
            flash(error)
            print("no hay usuario")
            return render_template('SearchUser.html')

        searchUser = str(searchUser)
        #en caso que no busco el usuario en la base de datos
        query = 'SELECT * FROM usuario WHERE usuario = "' + searchUser + '"'
        user_dataBase = db_Activa.execute(query).fetchone()
    

        #valido que encontré un usuario
        if user_dataBase is None:
            #en caso que no lo encuentre aviso que no lo encontré y me quedo en la misma página 
            error = 'Usuario no existe'
            print(error)
            flash(error)
            return render_template('SearchUser.html')
        else: 
            #si lo encontré guardo su Id y me voy a la `página de editar`

            #opción1
            #url_update_user = "UpdateUser/" + searchUser
            #return redirect(url_update_user)

            #opción2
            return redirect(url_for('UpdateUser', usuario_buscar = searchUser))
        
    else:    
        return render_template("SearchUser.html")   

@app.route("/UpdateUser",methods=["GET","POST",])
def UpdateUser():

    print('Entro a update user method')
    searchUser = request.args.get('usuario_buscar')
    
    if request.method == 'POST':
        #si el valor del botón es update significa que dio click en actualizar
        if request.form["boton"] == 'Update':
            print("la comparación tomó el valor de update")
            #de entrar acá hay que editar el usuario
            print('Entro a update user method con método post')
            updateUserName = request.form["NewUserName"]
            updateUserUser = request.form["NewUserUser"]
            updateUserPassword = request.form["NewUserPassword"]
            updateUserMail = request.form["NewUserMail"]
            #hacer la consulta 
            close_db()
            db_Activa = get_db()

            #valido que no estén vacios los campos
            if not updateUserName: 
                error = "El nombre es requerido"
                flash(error)
                print("no hay nombre")
                return redirect(url_for('UpdateUser', usuario_buscar = searchUser))

            if not updateUserUser: 
                error = "El usuario es requerido"
                flash(error)
                print("no hay usuario")
                return redirect(url_for('UpdateUser', usuario_buscar = searchUser))

            if not updateUserPassword: 
                error = "La contraseña es requerida"
                flash(error)
                print("no hay contraseña")
                return redirect(url_for('UpdateUser', usuario_buscar = searchUser))

            if not updateUserMail: 
                error = "El mail es requerido"
                flash(error)
                print("no hay mail")
                return redirect(url_for('UpdateUser', usuario_buscar = searchUser)) 

            #voy a transformar la clave en un hash para mayor segurar
            hash_password = generate_password_hash(updateUserPassword)
            updateUserPassword = hash_password

            query = 'UPDATE usuario SET nombre = "' + updateUserName + '", usuario = "' + updateUserUser + '", correoElectronico = "' + updateUserMail + '", contraseña = "' + updateUserPassword + '" WHERE usuario = "' + searchUser +'";'
            print(query)
            user_dataBase = db_Activa.execute(query)
            db_Activa.commit()
            close_db()

            flash('Usuario editado con éxito')

            return redirect("/SearchUser")

        elif request.form['boton'] == 'Delete':

            print("la comparación tomó el valor de delete")
            close_db()
            db_Activa = get_db()

            #hace la consulta para encontrar el ID del usuario dado un usuario
            query = 'SELECT id FROM usuario WHERE usuario = "' + searchUser + '";'
            print(query)
            user_dataBase = db_Activa.execute(query).fetchone()
            id_buscado = user_dataBase[0]
            print("el id buscado es " + str(id_buscado))

            #hacer la consulta para eliminar de la tabla Roles primero (con mayúscula)
            query = 'DELETE FROM Roles WHERE id_usuario = ' + str(id_buscado) + ';'
            print(query)
            user_dataBase = db_Activa.execute(query)
            db_Activa.commit()
            

            #ahora hago la consulta para eliminar de la tabla de usuarios
            query = 'DELETE FROM usuario WHERE id = ' + str(id_buscado) + ';'
            print(query)
            user_dataBase = db_Activa.execute(query)
            db_Activa.commit()
            close_db()

            print("Eliminación exitosa")
            flash("Eliminación exitosa")

            return redirect("/SearchUser")
        else: 
            print('la comparación no sirvió de nada :)')
            return redirect("/")

        
        
    else:
        print('Entro a update user method con método get y parametro ' + searchUser)
        return render_template("UpdateUser.html")
    

@app.route("/UpdateUser",methods=["GET","POST"])
def UpdateUser2():
    return render_template("SearchUser.html")

@app.route("/NewProduct",methods=["GET","POST"])  
def NewProduct():
    if request.method == "POST":
        NewProductName = request.form["NewProductName"]
        NewQuantity = request.form["NewProductQuantity"]
        NewImage = request.form["NewProductImage"]
        return redirect("HomeAdmin")
    else:    
        return render_template("NewProduct.html")

@app.route("/UpdateProduct",methods=["GET","POST"])
def UpdateProduct():
    if request.method == "POST":
        UpdateProductName = request.form["NewProductName"]
        UpdateQuantity = request.form["NewQuantity"]
        UpdateImage = request.form["NewImage"]
    else:    
        return render_template("UpdateProduct.html")

@app.route("/UpdateProductUser",methods=["GET","POST"])
def UpdateProductUser():
    if request.method == "POST":
        UpdateQuantity = request.form["NewQuantity"]
    else:    
        return render_template("UpdateProductUser.html") 

@app.route("/SearchProduct",methods=["GET","POST"])
def SearchProduct():
    if request.method == "POST":
        #searchUser = request.form["id"]
        return redirect("UpdateProduct")
    else:    
        return render_template("SearchProduct.html")




#Inicio de métodos para validar usuario y contraseña-------------------------------

#Este método valida en el momento que se llame si hay un usuario conectado, en caso que no me manda a la página de login. 
#se debe importar session y g
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            #si no hay un usuario conectado me manda a la página del login
            #en este caso la página de login es la página inicial del programa
            return redirect(url_for('/'))
        return view(**kwargs)
    return wrapped_view






#Fin de métodos para validar usuario y contraseña------------------------------------

        

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
