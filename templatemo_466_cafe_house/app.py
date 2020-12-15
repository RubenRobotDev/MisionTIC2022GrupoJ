from flask import Flask as fl
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/sql/databaseusuario.db"

app = fl(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    correoelectronico = db.Column(db.String(50), unique=True)
    contraseña = db.Column(db.String(30), nullable=False)
    

@app.route("/",methods=["GET","POST"])
def hello():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["pass"]
        return redirect(url_for("HomeAdmin"))
    else:
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
        User=Usuario
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
    if request.method == "POST":
        searchUser = request.form["search"]
        return redirec("UpdateUser")
    else:    
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

@app.route("/UpdateUser",methods=["GET","POST"])
def UpdateUser():
    if request.method == "POST":
        updateUserName = request.form["NewUserName"]
        updateUserUser = request.form["NewUserUser"]
        updateUserPassword = request.form["NewUserPassword"]
        updateUserMail = request.form["NewUserMail"]
    else:    
        return render_template("UpdateUser.html")

        

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
