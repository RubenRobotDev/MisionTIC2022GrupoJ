from flask import Flask as fl
from flask import render_template, request
import os


app = fl(__name__)

@app.route("/",methods=['GET', 'POST'])   
def hello():
    if request.method=="POST":
        user=request.form["user"]
    print(user)
    return render_template("login.html")

@app.route("/RecoverPassword")
def RecoverPassword():
    return render_template("RecoverPassword.html")

@app.route("/HomeAdmin")
def HomeAdmin():
    return render_template("HomeAdmin.html")

@app.route("/HomeUser")
def HomeUser():
    return render_template("HomeUser.html")

@app.route("/ManageUser")
def ManageUser():
    return render_template("ManageUser.html")

@app.route("/NewUser")
def NewUser():
    return render_template("NewUser.html")

@app.route("/SearchUser")
def SearchUser():
    return render_template("SearchUser.html")


   

@app.route("/NewProduct")  
def NewProduct():
    return render_template("NewProduct.html")

@app.route("/UpdateProduct")
def UpdateProduct():
    return render_template("UpdateProduct.html")

@app.route("/UpdateProductUser")
def UpdateProductUser():
    return render_template("UpdateProductUser.html") 

@app.route("/SearchProduct")
def SearchProduct():
    return render_template("SearchProduct.html")

@app.route("/UpdateUser")
def UpdateUser():
    return render_template("UpdateUser.html")

if __name__ == "__main__":
    app.run(debug=True)
