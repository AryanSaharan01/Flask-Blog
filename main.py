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

@app.route("/pricing")
def pricing():
    return render_template('pricing.html')

@app.route("/service")
def service():
    return render_template('service.html')

@app.route("/project")
def project():
    return render_template('project.html')

@app.route("/blog-grid")
def blogGrid():
    return render_template('blog-grid.html')

@app.route("/blog-sidebar")
def blogSidebar():
    return render_template('blog-sidebar.html')

@app.route("/blog-single")
def blogSingle():
    return render_template('blog-single.html')






# it will update any changes
app.run(debug=True)
