from flask_restful import reqparse
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime
from app import db, ma


class Course(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    start_time: Mapped[DateTime] = db.Column(db.DateTime, server_default=None)
    end_time: Mapped[DateTime] = db.Column(db.DateTime, server_default=None)
    prof_assign = db.relationship('ProfessorAssignment', backref='course', lazy=True)
    stud_enroll = db.relationship('StudentEnrollment', backref='course', lazy=True)
    attendance = db.relationship('Attendance', backref='course', lazy=True)


class CourseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course

    id = fields.Integer()
    start_time = fields.DateTime()
    end_time = fields.DateTime()

    @post_load
    def make_model(self, data, **kwargs):
        return Course(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('start_time', type=DateTime, location='json')
        parser.add_argument('end_time', type=DateTime, location='json')
        return parser
