from flask_restful import reqparse
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from app import db, ma


class Professor(db.Model):
    professor_id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    first_name: Mapped[str] = db.Column(db.String(32), nullable=False)
    last_name: Mapped[str] = db.Column(db.String(32), nullable=False)
    email: Mapped[str] = db.Column(db.String(32))
    many_to_many = db.relationship('ProfessorAssignment', backref='professor', lazy=True)


class ProfessorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Professor

    professor_id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String()

    @post_load
    def make_model(self, data, **kwargs):
        return Professor(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        return parser
