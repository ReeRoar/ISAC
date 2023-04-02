from flask_login import UserMixin
from flask_restful import reqparse, inputs
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime
from app import db, ma
from models.course import Course, CourseSchema
from models.professor import Professor
from models.student import Student, StudentSchema


class User(UserMixin, db.Model):
    email = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.professor_id"), nullable=True)
    id = email


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    email = fields.String()
    password = fields.String()
    professor_id = fields.Integer()

    @post_load
    def make_model(self, data, **kwargs):
        return User(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('professor_id', type=int, location='json')
        parser.add_argument('password', type=int, location='json')
        return parser


class UserProfSchema(ma.SQLAlchemySchema):
    class Meta:
        user = User
        prof = Professor

    Course = fields.Nested(User)
    Student = fields.Nested(Professor)


class UserPasswordSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    email = fields.String()
    password = fields.String()

    @post_load
    def make_model(self, data, **kwargs):
        return User(**data)


