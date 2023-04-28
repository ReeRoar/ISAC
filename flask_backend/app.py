from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
db = SQLAlchemy()

app = Flask(__name__)
ma = Marshmallow(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root@localhost/flask_test'
app.config['SECRET_KEY'] = 'my_key' #HARDCODED FOR NOW CHANGE TO ENV VARIABLE ON PI

db.init_app(app)


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res
