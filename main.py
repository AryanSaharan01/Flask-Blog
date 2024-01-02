from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():   #the def fuction name should be different in each new app
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/post")
def pricing():
    return render_template('post.html')








# it will update any changes
app.run(debug=True)
