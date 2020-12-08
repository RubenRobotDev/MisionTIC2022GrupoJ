from flask import Flask as fl
from flask import render_template
import os


app = fl(__name__)

@app.route("/")
def hello():
    return render_template("login.html")

@app.route("/UpdateProduct")
def UpdateProduct():
    return render_template("UpdateProduct.html")

if __name__ == "__main__":
    app.run(debug=True)
