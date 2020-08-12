from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_mail import Mail
import json
import os
import math


with open('config.json','r') as c:
    params =json.load(c)["params"]

local_server = True

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME= params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'])

mail = Mail(app)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):

#here class name should be same with the name of database table
#or use this sintax to mention it: __tablename__ = "contents"

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    sub_heading = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)
    # author = db.Column(db.String(12), nullable=True)
    # author_slug = db.Column(db.String(21), nullable=False)

class main_nav(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    main_header = db.Column(db.String(80), nullable=False)
    main_subheading = db.Column(db.String(80), nullable=False)
    main_img = db.Column(db.String(12), nullable=True)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name= db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    re_password = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    post = Posts.query.filter_by().all()
    last = math.ceil(len(post)/int(params['no_of_posts']))
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    post =post[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+int(params['no_of_posts'])]
    if (page == 1):
        prev = "#"
        next = "/?page="+str(page+1)
    elif (page == last):
        prev = "/?page="+str(page-1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    Main_nav = main_nav.query.filter_by().first()
    return render_template('index.html', params = params, post = post, main_nav = Main_nav,prev =prev,next =next)



@app.route("/author")
def author():
    post = Posts.query.first()

    return post.author


@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()

    return render_template('post.html', params = params , post = post)

# @app.route("/author/<string:author_slug>", methods = ['GET'])
# def author_route(author_slug):
#     post = Posts.query.filter_by(slug = author).first()
#     return render_template('author.html', params = params , post = post)


@app.route("/about")
def about():
    return render_template('about.html', params = params)

# @app.route("/dashboard")
# def dashboard():
#     # regist = Register.query.filter_by().all()
#     regist = Register.query.first()
#     named = regist.first_name
#     print(named)
#     return render_template('admin/login.html', params=params, regist = regist,named = named)
# dashboard()

@app.route("/dashboard", methods  = ['GET','POST'])
def login():
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('admin/index.html', params = params)

    regist = Register.query.filter_by().first()
    named = regist.first_name
    passd = regist.password

    if request.method == 'POST':
        username = request.form.get('myname')
        userpass = request.form.get('pass')
        if (username == named and userpass == passd):
            session['user'] = username
            return render_template('admin/index.html', params = params, regist = regist, named =named, passd = passd)

    return render_template('admin/login.html', params = params)


@app.route("/register", methods = ['GET','POST'])
def register():
    if (request.method == 'POST'):
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        emailaddress = request.form.get('emailaddress')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        add_to_db = Register(first_name = firstname, last_name = lastname, email_address = emailaddress,
                             password = password, re_password = repassword,date= datetime.now())
        db.session.add(add_to_db)
        db.session.commit()
        return redirect('/dashboard')


    return render_template('admin/register.html')

@app.route("/forgot-password")
def forgotpassword():
    return render_template('admin/forgot-password.html')

@app.route("/dashboard/table")
def table():
    if ('user' in session and session['user'] == params['admin_user']):
        post = Posts.query.all()
        return render_template('admin/tables.html', params = params, posts = post)

    return render_template('admin/login.html', params = params)

@app.route("/dashboard/edit/<string:sno>", methods = ['GET','POST'])
def edit(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            box_title = request.form.get('title')
            subheading = request.form.get('subheading')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == '0':
                post = Posts(title = box_title, slug = slug, content = content,
                              sub_heading = subheading, img_file = img_file, date = date)

                db.session.add(post)
                db.session.commit()

            else:
                post = Posts.query.filter_by(sno = sno).first()
                post.title = box_title
                post.slug = slug
                post.content = content
                post.sub_heading = subheading
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect('/dashboard/edit/'+sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('/admin/edit.html', params = params, post = post, sno =sno)

    return render_template('admin/login.html', params=params)


@app.route("/uploader", methods = ['GET', 'POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_user']):
        if (request.method == 'POST'):
            f= request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded Successfully"
    return render_template('admin/login.html', params=params)


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

@app.route("/dashboard/deletepost/<string:sno>", methods = ['GET', 'POST'])
def deletepost(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        post = Posts.query.filter_by(sno = sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard/table')

@app.route("/newpost")
def newpost():
    if ('user' in session and session['user'] == params['admin_user']):
        return redirect('/dashboard/edit/0')
    return render_template('admin/login.html', params=params)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name + ', Email_address: ' + email,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + 'From:' + phone
                          )
    return render_template('contact.html', params = params)

app.run(debug=True)