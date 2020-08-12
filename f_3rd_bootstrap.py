from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/about")
def Harshit():
    return render_template('about.html')

@app.route("/bootstrap")
def myfunction():
    return render_template('bootstrap.html')

app.run(debug = True)