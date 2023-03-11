from flask import Flask, request, jsonify, abort
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import json
from GenericRequest import GenericRequest
from flask_marshmallow import Marshmallow
from flask_restful import reqparse
from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    post_dump,
    post_load,
    ValidationError,
)

db = SQLAlchemy()

app = Flask(__name__)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:password@localhost/flask_test'

db.init_app(app)


@app.route('/<name>')
def hello_world(name):
    return f'<p> hello {escape(name)} </p>'


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(32))


class ModelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Model

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()

    @post_load
    def make_model(self, data, **kwargs):
        return Model(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('id', type=int, location='json')
        return parser


with app.app_context():
    db.create_all()

model_generic = GenericRequest(Model, ModelSchema(), db, True)


@app.route('/models', methods=['GET', 'POST'])
def models():
    if request.method == 'GET':
        return model_generic.get_all()
    if request.method == 'POST':
        return model_generic.post_request(request)


@app.route('/models/<model_id>', methods=['GET', 'DELETE', 'PUT'])
def models_id(model_id):
    if request.method == 'GET':
        return model_generic.get_by_id(model_id)
    if request.method == 'PUT':
        return model_generic.put_request(model_id)
    if request.method == 'DELETE':
        return model_generic.delete_request(model_id)


if __name__ == '__main__':
    app.run(debug=True)
