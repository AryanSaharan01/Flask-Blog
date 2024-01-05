from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
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
    content_2 = db.Column(db.String(400), nullable=False)
    content_3 = db.Column(db.String(400), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    # img = db.Column(db.String(1000), nullable=True)


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    return render_template("index.html", params=params, posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", params=params)


@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template("post.html", params=params, post=post)
# http://127.0.0.1:5000/post/first-post..............in order to access post


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
