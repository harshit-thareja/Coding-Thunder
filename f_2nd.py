from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")        #the endpoint if the website

def hello():
    return render_template('index.html')   #"render_temp" is use to open(fatch)the file


@app.route("/about")          #another endpoint

#    PASS VARIABLES IN A TAMPLATE(BY JINJA)

# jinja template is nothing it just a way to use programing through our template..
#..(HTML document) like for loop etc.


def Harshit():
    Name = 'Aryan'     #here we declare the name as Aryan
    return render_template('about.html', name = Name) #here we call 'Name' by 'name'..
                                                      #..which is stored in template as 'name'

app.run(debug = True)  #from "debug = True" it will refresh automatically when any change occur
