from flask import Flask

app = Flask(__name__)

@app.route("/")      #the endpoint if the website

def hello():
    return "HELLO WORLD!"


@app.route("/harshit")          #another endpoint
def Harshit():
    return "HELLO HARSHIT!"
app.run(debug = True)  #from "debug = True" it will refresh automatically when any change occur


