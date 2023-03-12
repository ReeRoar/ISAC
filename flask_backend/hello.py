from typing import List

from flask import Flask, request, jsonify, abort
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import json
from ManyToOneRequest import ManyToOneRequest
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry

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
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32))
    one_to_manys = db.relationship('ManyToOneModel', backref='model', lazy=True)


class ManyToOneModel(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    info: Mapped[str] = db.Column(db.String(32))
    model_id = db.Column(db.Integer,db.ForeignKey("model.id"),nullable=False)


class ModelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Model

    id = fields.Integer()
    username = fields.String()
    email = fields.String()

    @post_load
    def make_model(self, data, **kwargs):
        return Model(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('id', type=int, location='json')
        return parser

class ManyToOneSchema(ma.SQLAlchemySchema):
    class Meta:
        many_to_one_model = ManyToOneModel
    id = fields.Integer()
    info = fields.String()
    model_id = fields.Integer()


    @post_load
    def make_model(self, data, **kwargs):
        return ManyToOneModel(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('info', type=str, location='json')
        parser.add_argument('model_id', type=int, location='json')
        return parser


class JoinedModelsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Model
        many_to_one_model = ManyToOneModel
    Model = fields.Nested(ModelSchema)
    ManyToOneModel = fields.Nested(ManyToOneSchema)


with app.app_context():
    db.create_all()

model_generic = GenericRequest(Model, ModelSchema(), db, True)
many_to_one_generic = GenericRequest(ManyToOneModel,ManyToOneSchema(),db,False)
many_to_model_requester = ManyToOneRequest(ManyToOneModel, ManyToOneSchema(), db, Model, JoinedModelsSchema(), has_reqparse=False)


@app.route('/models_many', methods=['GET', 'POST'])
def models_many():
    if request.method == 'GET':
        return many_to_one_generic.get_all()
    if request.method == 'POST':
        return many_to_one_generic.post_request(request)

@app.route('/joined', methods=['GET', 'POST'])
def joined_models():
    if request.method == 'GET':
        return many_to_model_requester.get_all_joined()

@app.route('/joined/<model_id>', methods=['GET', 'POST'])
def joined_models_one_id(model_id):
    if request.method == 'GET':
        return many_to_model_requester.get_all_joined_by_one_model_id(model_id)

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
