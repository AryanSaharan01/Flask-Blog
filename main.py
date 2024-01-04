from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


local_server = True
with open('config.json' , 'r') as c:
    params = json.load(c) ["params"]

app = Flask(__name__)
if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params ["local_uri"]

else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params ["prod_uri"]

db = SQLAlchemy(app)


class Contact(db.Model):
    """
    sno, name phone_no, msg, date, email
    """

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def index():  # the def fuction name should be different in each new app
    return render_template("index.html" , params=params)


@app.route("/about")
def about():
    return render_template("about.html" , params=params)


@app.route("/post")
def pricing():
    return render_template("post.html" , params=params)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        """Add entry to the database"""
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        entry = Contact(
            name=name, phone_no=phone, msg=message, date=datetime.now(), email=email
        )
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html" , params=params)


# it will update any changes
app.run(debug=True)
