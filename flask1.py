from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/Aryan")
def heyy():
    return "Heyy! Aryan....how are oooo"
# you need to type this in order to print this
# http://127.0.0.1:5000/Aryan

'''<ul>
{% for user in users %}
  <li><a href="{{ user.url }}">{{ user.username }}</a></li>
{% endfor %}
</ul>'''

# <img src="{{ url_for('static', filename='img_name.png') }}">


# app.run()

# it will take any changes
app.run(debug=True)
