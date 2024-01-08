from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail
import json
import math

import os
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']


app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME="flasktutorial00@gmail.com",
    MAIL_PASSWORD="jegh obav jada qyfq"
)
mail = Mail(app)
if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]
db = SQLAlchemy(app)
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    subheading = db.Column(db.String(100), nullable=False)
    written_by = db.Column(db.String(40), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    overview = db.Column(db.String(500), nullable=False)
    heading_1 = db.Column(db.String(50), nullable=False)
    content_1 = db.Column(db.String(600), nullable=False)
    heading_2 = db.Column(db.String(50), nullable=False)
    content_2 = db.Column(db.String(800), nullable=False)
    content_3 = db.Column(db.String(800), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    # img = db.Column(db.String(1000), nullable=True)
# @app.route("/")
# def home():
#     posts = Posts.query.filter_by().all() [0:3]
#     return render_template("index.html", params=params, posts=posts)




@app.route("/about")
def about():
    return render_template("about.html", params=params)

@app.route("/login", methods=["GET", "POST"])
def login():

    if ('user' in session and session['user'] == params["admin_user"]):
        posts = Posts.query.all()
        return render_template("dashboard.html", params=params, posts = posts)
    if request.method=='POST':
        username = request.form.get("username")
        userpswd = request.form.get("pswd")
        if (username == params["admin_user"] and userpswd == params["admin_password"]):
            # set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template("dashboard.html", params=params, posts = posts)
    return render_template("login.html", params=params)
@app.route("/allposts")
def allpost():
    posts = Posts.query.filter_by().all()
    return render_template("allposts.html", params=params, posts=posts)


@app.route("/edit/<string:sno>",  methods=["GET", "POST"])
def edit(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            box_title = request.form.get('title')
            subheading = request.form.get('subheading')
            written_by = request.form.get('written_by')
            slug = request.form.get('slug')
            overview = request.form.get('overview')
            heading_1 = request.form.get('heading_1')
            content_1 = request.form.get('content_1')
            heading_2 = request.form.get('heading_2')
            content_2 = request.form.get('content_2')
            content_3 = request.form.get('content_3')
            date = datetime.now()

            if sno=='0':
                post = Posts(
                    title=box_title,
                    subheading=subheading,
                    written_by=written_by,
                    slug=slug,
                    overview=overview,
                    heading_1=heading_1,
                    content_1=content_1,
                    heading_2=heading_2,
                    content_2=content_2,
                    content_3=content_3,
                    date=date
                )
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.subheading = subheading
                post.written_by = written_by
                post.slug = slug
                post.overview = overview
                post.heading_1 = heading_1
                post.content_1 = content_1
                post.heading_2 = heading_2
                post.content_2 = content_2
                post.content_3 = content_3
                post.date = date
                db.session.commit()
                return redirect('/edit/'+sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post, sno=sno)



@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template("post.html", params=params, post=post)
# http://127.0.0.1:5000/post/first-post..............in order to access post




# @app.route("/uploader" , methods=['GET', 'POST'])
# def uploader():
#     if "user" in session and session['user']==params['admin_user']:
#         if request.method=='POST':
#             f = request.files['file1']
#             f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
#             return "Uploaded successfully!"


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if "user" in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return render_template("successfull.html")
        # Handle other HTTP methods if needed
    # Handle the case where the user is not logged in
    return redirect("/")  # Redirect to home if not logged in



@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/login')


@app.route("/delete/<string:sno>",  methods=["GET", "POST"])
def delete(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/login')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        entry = Contact(
            name=name, phone_no=phone, msg=message, date=datetime.now(), email=email
        )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=["flasktutorial00@gmail.com"],
                          body=message + "\n" + phone
                          )
    return render_template("contact.html", params=params)
if __name__ == "__main__":
    app.run(debug=True)