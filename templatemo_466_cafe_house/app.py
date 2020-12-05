from flask import Flask as fl

app = fl(__name__)

@app.route("/")
def hello():
    return "Hello world"
if __name__ == '__main__':
    app.run(debug=True)
