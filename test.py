from flask import Flask 
from flask_mailman import Mail, EmailMessage

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "flasktutorial00@gmail.com"
    app.config["MAIL_PASSWORD"] = "fl@sktut0"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail.init_app(app)

    @app.route("/")
    def index():
        msg = EmailMessage(
            "Here's the title!",
            "Body of the email",
            "from@email.com",
            ["saharan01kng@email.com"]
        )
        msg.send()
        return "Sent email..."

    return app