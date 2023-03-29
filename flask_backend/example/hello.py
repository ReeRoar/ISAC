from typing import List

from flask import Flask, request, jsonify, abort
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import json
from generic_requests.ManyToOneRequest import ManyToOneRequest
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry
from generic_requests.ManyToManyRequest import ManyToManyRequest
from generic_requests.GenericRequest import GenericRequest
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


class Model(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32))
    one_to_manys = db.relationship('ManyToOneModel', backref='model', lazy=True)
    many_to_many = db.relationship('ManyToManyModel', backref='model', lazy=True)


class ManyToOneModel(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    info: Mapped[str] = db.Column(db.String(32))
    model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)


class SampleModel(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    text: Mapped[str] = db.Column(db.String(32), nullable=False)
    many_to_many = db.relationship('ManyToManyModel', backref='sample_model', lazy=True)


class ManyToManyModel(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    model2_id = db.Column(db.Integer, db.ForeignKey("sample_model.id"), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)


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


class SampleModelSchema(ma.SQLAlchemySchema):
    class Meta:
        sample_model = SampleModel

    id = fields.Integer()
    text = fields.String()

    @post_load
    def make_model(self, data, **kwargs):
        return SampleModel(**data)


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


class ManyToManyModelSchema(ma.SQLAlchemySchema):
    class Meta:
        m2m = ManyToManyModel

    id = fields.Integer()
    model_id = fields.Integer()
    model2_id = fields.Integer()

    @post_load
    def make_model(self, data, **kwargs):
        return ManyToManyModel(**data)


class JoinedModelsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Model
        many_to_one_model = ManyToOneModel

    Model = fields.Nested(ModelSchema)
    ManyToOneModel = fields.Nested(ManyToOneSchema)


class ManyToManyJoinedSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Model
        sample_model = SampleModel
        many_to_many_model = ManyToManyModel

    Model = fields.Nested(ModelSchema)
    SampleModel = fields.Nested(SampleModelSchema)
    ManyToManyModel = fields.Nested(ManyToManyModelSchema)


with app.app_context():
    db.create_all()

model_generic = GenericRequest(Model, ModelSchema(), db, True)
many_to_one_generic = GenericRequest(ManyToOneModel, ManyToOneSchema(), db, False)
sample_model_requester = GenericRequest(SampleModel, SampleModelSchema(), db, False)
many_to_many_requester = GenericRequest(ManyToManyModel, ManyToManyModelSchema(), db, False)
many_to_model_requester = ManyToOneRequest(ManyToOneModel, ManyToOneSchema(), db, Model, JoinedModelsSchema(),
                                           has_reqparse=False)
many_to_many_join_requester = ManyToManyRequest(Model, ModelSchema(), SampleModel, SampleModelSchema(),
                                                ManyToManyModel, ManyToManyJoinedSchema(), db, False)


@app.route('/many_to_many', methods=['GET', 'POST'])
def many_to_many_add():
    if request.method == 'GET':
        return many_to_many_requester.get_all()
    if request.method == 'POST':
        return many_to_many_requester.post_request(request)


@app.route('/sample_add', methods=['GET', 'POST'])
def sample_add():
    if request.method == 'GET':
        return sample_model_requester.get_all()
    if request.method == 'POST':
        return sample_model_requester.post_request(request)


@app.route('/many_to_many_get', methods=['GET'])
def get_many_to_many():
    if request.method == 'GET':
        return many_to_many_join_requester.get_all_joined()


@app.route('/many_to_many_get/<id>', methods=['GET'])
def get_many_to_many_id(id):
    if request.method == 'GET':
        return many_to_many_join_requester.get_all_joined_by_model_id(id)


@app.route('/many_to_many_get2/<id>', methods=['GET'])
def get_many_to_many_id2(id):
    if request.method == 'GET':
        return many_to_many_join_requester.get_all_joined_by_model2_id(id)


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
