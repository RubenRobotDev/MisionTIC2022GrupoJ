from flask import Flask as fl
from flask import render_template, request, redirect, url_for, session, g
from flask import flash
from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from db import close_db
from db import get_db
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
import os

####################################################################
###### Inicializacion del sistema para manejo de aplicaciones ######
####################################################################

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/sql/databaseusuario.db"
UPLOAD_FOLDER = os.path.abspath("./static/img/uploads/")


app = fl(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = os.urandom(24)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30))
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    correoelectronico = db.Column(db.String(50), unique=True)
    contraseña = db.Column(db.String(30), nullable=False)


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True)
    cantidad = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(100))

class Roles(db.Model):
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    rol = db.Column(db.String(30))

class Log():
    log=False
    admin=False

log = Log()

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
            flash(error,"success")
            print("no hay usuario")
            return render_template('login.html')

        if not password: 
            error = "La clave es requerida"
            flash(error,"success")
            print("no hay clave")
            return render_template('login.html')

        #hago la consulta a la base de datos para ver si el usuario existe
        query = 'SELECT * FROM usuario WHERE usuario = "' + user + '"'
        user_dataBase = db_Activa.execute(query).fetchone()
        
        if user_dataBase is None:
            error = 'Usuario o contraseña inválidos'
            print(error)
            flash("Usuario o contraseña inválidos", "error")
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
                print(tipo_usuario[1])
                log.log=True
                if tipo_usuario[1] == "Admin":
                    log.admin = True
                    return redirect(url_for("HomeAdmin"))
                else: 
                    return redirect(url_for("HomeUser"))
            else: 
                error = 'Usuario o contraseña inválidos v2'
                print(error)
                flash(error,"success")
                return render_template("login.html")
    else: 
        log.log = False
        log.admin = False
        print('no mandó un método post')
        return render_template("login.html")
    
####################################################################
############ Sistema base para recuperar la contraseña #############
####################################################################

  

@app.route("/RecoverPassword",methods=["GET","POST"])
def RecoverPassword():
    ### Solicitamos por el metodo Post el correo elecrtronico para reestablecer la contraseña
    if request.method == "POST":
        mail = request.form["email"]
        return redirect(url_for("hello"))
    else:    
        return render_template("RecoverPassword.html")

####################################################################
######################## Sistema de inicio #########################
####################################################################

@app.route("/HomeAdmin")
def HomeAdmin():
    if not log.log:
        return redirect(url_for("hello"))
    return render_template("HomeAdmin.html")

@app.route("/HomeUser")
def HomeUser():
    if not log.log:
        return redirect(url_for("hello"))
    return render_template("HomeUser.html")

@app.route("/Home")
def Home():
    if log.admin:
        return redirect(url_for("HomeAdmin"))
    else:
        return redirect(url_for("HomeUser"))


@app.route("/ManageUser",methods=["GET","POST"])
def ManageUser():
    if not log.log:
        return redirect(url_for("hello"))
    if request.method == "POST":
        return render_template("ManageUser.html")
    else:    
        return render_template("ManageUser.html")

#crear nuevo usuario
@app.route("/NewUser",methods=["GET","POST"])
def NewUser():
    if not log.log:
        return redirect(url_for("hello"))
    if request.method == "POST":
        User=Usuario()
        newUserName = request.form["NewUserName"]
        newUserUser = request.form["NewUserUser"]
        newUserPassword = request.form["NewUserPassword"]
        newUserMail = request.form["NewUserMail"]

        hash_password = generate_password_hash(newUserPassword)
        newUserPassword = hash_password

        User.nombre = request.form["NewUserName"]
        User.usuario = newUserUser
        User.contraseña = newUserPassword
        User.correoelectronico = newUserMail

        db.session.add(User)
        db.session.commit()
        close_db()

    
        db_Activa = get_db()
        query = 'SELECT id FROM usuario WHERE usuario = "'+ str(newUserUser)+ '";'
        usuario_creado = db_Activa.execute(query).fetchone()
        id0 = usuario_creado[0]
        query2 = 'INSERT INTO Roles (id_usuario,rol) VALUES ('+str(id0)+',"User");'
        usuario_creado = db_Activa.execute(query2)
        db_Activa.commit()

        return redirect("/NewUser")

    else:    
        return render_template("NewUser.html")


@app.route("/SearchUser",methods=["GET","POST"])
def SearchUser():
    if not log.log:
        return redirect(url_for("hello"))
    print('Entro a search User method')

    close_db()
    db_Activa = get_db()
    
    
    if request.method == 'POST':
        print('Entro a POST search User method')
        #search user tiene usuario que se busca
        try:
            searchUser = request.form["search"]
        except Exception as e:
            print("el error es " + str(e))

        #valido que no esté vacio
        if not searchUser: 
            error = "El usuario es requerido"
            flash(error,"success")
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
            flash(error,"success")
            return render_template('SearchUser.html')
        else: 
            #si lo encontré guardo su Id y me voy a la `página de editar`
            #paso más parámetros para que se vean en la aplicación
            print(user_dataBase[1])
            namePresentar = str(user_dataBase[1])
            userPresentar = str(user_dataBase[2])
            passwordPresentar = str(user_dataBase[4])
            mailPresentar = str(user_dataBase[3])

            #opción1
            #url_update_user = "UpdateUser/" + searchUser
            #return redirect(url_update_user)

            #opción2
            return render_template('UpdateUser.html', currentUser = searchUser , currentName = namePresentar, currentMail = mailPresentar)
            #return redirect(url_for('UpdateUser', usuario_buscar = searchUser, nameFormulario = namePresentar, userFormulario = userPresentar, passwordFormulario = passwordPresentar, mailFormulario = mailPresentar))
        
    else:    
        print("Entro a search user como un get")
        return render_template("SearchUser.html")   

@app.route("/UpdateUser",methods=["GET","POST",])
def UpdateUser():
    if not log.log:
        return redirect(url_for("hello"))

    print('Entro a update user method')
    #searchUser = request.args.get('usuario_buscar')
    
    if request.method == 'POST':
        #si el valor del botón es update significa que dio click en actualizar
        if request.form["boton"] == 'Update':
            print("la comparación tomó el valor de update")
            #de entrar acá hay que editar el usuario
            print('Entro a update user method con método post')
            searchUser = request.form["CurrentUserName"]
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
                flash(error,"success")
                print("no hay nombre")
                return redirect(url_for('UpdateUser', usuario_buscar = searchUser))

            if not updateUserUser: 
                error = "El usuario es requerido"
                flash(error,"success")
                print("no hay usuario")
                return redirect(url_for('UpdateUser', usuario_buscar = searchUser))

            if not updateUserPassword: 
                error = "La contraseña es requerida"
                flash(error,"success")
                print("no hay contraseña")
                return redirect(url_for('UpdateUser', usuario_buscar = searchUser))

            if not updateUserMail: 
                error = "El mail es requerido"
                flash(error,"success")
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

            flash('Usuario editado con éxito',"success")

            return render_template("SearchUser.html")

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
            flash("Eliminación exitosa","success")

            return render_template("SearchUser.html")
        else: 
            print('la comparación no sirvió de nada :)')
            return redirect("/")

        
        
    else:
        print('Entro a update user method con método get y parametro ')
        return render_template("SearchUser.html")
    

@app.route("/UpdateUser",methods=["GET","POST"])
def UpdateUser2():
    if not log.log:
        return redirect(url_for("hello"))
    return render_template("SearchUser.html")

@app.route("/NewProduct",methods=["GET","POST"])  
def NewProduct():
    if not log.log:
        return redirect(url_for("hello"))
    if request.method == "POST":
        productodb=Producto()
        productodb.nombre = request.form["NewProductName"]
        productodb.cantidad = request.form["NewProductQuantity"]
        f = request.files["NewProductImage"]

        if productodb.nombre == "":
            flash("Falta completar el nombre del producto", "error")
            return redirect(url_for("NewProduct"))
        if productodb.cantidad == "":
            flash("Falta especificar la cantidad del producto", "error")
            return redirect(url_for("NewProduct"))
        if "NewProductImage" not in request.files:
            flash("El formulario no tiene ningún archivo", "error")
            return redirect(url_for("NewProduct"))
        if f.filename == "":
            flash("Ningún archivo seleccionado", "error")
            return redirect(url_for("NewProduct"))

        productodb.path = f.filename
        f.save(os.path.join(UPLOAD_FOLDER, productodb.path))
        db.session.add(productodb)
        db.session.commit()

        flash("Su producto se ha agregado correctamente", "success")
        return redirect(url_for("NewProduct"))
    return render_template("NewProduct.html")

@app.route("/SearchProduct",methods=["GET","POST"])
def SearchProduct():
    if not log.log:
        return redirect(url_for("hello"))
    if request.method == "POST":
        nombre = request.form["nombreproducto"]
        producto = Producto.query.filter_by(nombre=nombre).first()
        if producto is None:
            flash("El producto no existe", "error")
            return render_template("SearchProduct.html")
        productoform=producto.nombre
        imagen = "static/img/uploads/" + producto.path
        if log.admin:
            print(log.admin)
            return render_template("UpdateProduct.html", id=producto.id, productoform = productoform, cantidad=producto.cantidad, imagen=imagen)
        else:
            print(log.admin)
            return render_template("UpdateProductUser.html", id=producto.id, productoform = productoform, cantidad=producto.cantidad, imagen=imagen)
        
    else:    
        return render_template("SearchProduct.html")



@app.route("/UpdateProduct",methods=["GET","POST"])
def UpdateProduct():
    if not log.log:
        return redirect(url_for("hello"))
    if request.method == "POST":
        productodb=Producto()
        #id = request.args.get("idproducto")
        #nombre = request.args.get("nombreproducto")
        #cantidad = request.args.get("cantidad")
        id = request.form["idproducto"]
        nombre = request.form["nombreproducto"]
        cantidad = request.form["cantidad"]

 
        f = request.files["imagenproducto"]
        if f.filename == "":
            producto = productodb.query.filter_by(id=id).update(dict(nombre=nombre, cantidad= cantidad))
        else:
            productodb.path = f.filename
            f.save(os.path.join(UPLOAD_FOLDER, productodb.path))
            producto = productodb.query.filter_by(id=id).update(dict(nombre=nombre, cantidad= cantidad, path=productodb.path))
        db.session.commit()

        flash("Su producto se ha actualizado correctamente", "success")
        return redirect(url_for("SearchProduct"))
        #return redirect(url_for("UpdateProduct", productoform = producto.nombre))
        
    else:
        return render_template("UpdateProduct.html")

@app.route("/DeleteProduct",methods=["GET","POST"])
def DeleteProduct():
    if not log.log:
        return redirect(url_for("hello"))
    if request.method == "POST":
        productodb=Producto()
        id = request.form["idproducto"]
        productodb.query.filter_by(id=id).delete()
        db.session.commit()
        flash("El producto se ha eliminado correctamente", "success")
    else:
        flash("El producto no se ha eliminó", "success")
    return redirect(url_for("SearchProduct"))




@app.route("/UpdateProductUser",methods=["GET","POST"])
def UpdateProductUser():
    if not log.log:
        return redirect(url_for("hello"))
    if request.method == "POST":
        productodb=Producto()

        id = request.form["idproducto"]
        cantidad = request.form["cantidad"]

        producto = productodb.query.filter_by(id=id).update(dict(cantidad= cantidad))
        db.session.commit()

        flash("La cantidad se ha actualizado correctamente", "success")
        return redirect(url_for("SearchProduct"))
        #return redirect(url_for("UpdateProduct", productoform = producto.nombre))
        
    else:
        return render_template("UpdateProductUser.html")






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

    #Creación usuario administrador por defecto
    User=Usuario()
    rol = Roles()
    administrator = User.query.filter_by(usuario='admin').first()
    if administrator is None:
        User.nombre = "Administrator"
        User.usuario = "admin"
        User.contraseña = generate_password_hash("Admin123")
        User.correoelectronico = "atdiego@uninorte.edu.co"
        db.session.add(User)
        db.session.commit()
        rol.id_usuario = 1
        rol.rol = "Admin"
        db.session.add(rol)
        db.session.commit()

    app.run(debug=True)
