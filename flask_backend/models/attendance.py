from flask_restful import reqparse
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime, Date, Boolean
from app import db, ma
from models import course
from models.course import Course, CourseSchema
from models.student import Student, StudentSchema


class Attendance(db.Model):
    """
    model id = course
    model id 2 = student
    """
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    date: Mapped[Date] = db.Column(db.Date)
    status: Mapped[str] = db.Column(db.String(1), server_default='Y')
    model_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    model2_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)


class AttendanceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Attendance

    id = fields.Integer()
    date = fields.Date()
    status = fields.String()
    model_id = fields.Integer()
    model2_id = fields.Integer()
    @post_load
    def make_model(self, data, **kwargs):
        return Attendance(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('date', type=Date, location='json')
        parser.add_argument('model_id', type=int, location='json')
        parser.add_argument('model2_id', type=int, location='json')
        parser.add_argument('status', type=str, location='json')
        return parser


class AttendanceJoinedSchema(ma.SQLAlchemySchema):
    class Meta:
        course = Course
        student = Student
        attendance = Attendance

    Course = fields.Nested(CourseSchema)
    Student = fields.Nested(StudentSchema)
    Attendance = fields.Nested(AttendanceSchema)