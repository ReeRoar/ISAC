from flask_restful import reqparse
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime
from app import db, ma
from models.course import Course, CourseSchema
from models.student import Student, StudentSchema


class StudentEnrollment(db.Model):
    """
    model_id = student id
    model2_id = course id
    """
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    model2_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)



class StudentEnrollmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StudentEnrollment

    id = fields.Integer()
    model2_id = fields.Integer()
    model_id = fields.Integer()

    @post_load
    def make_model(self, data, **kwargs):
        return StudentEnrollment(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('model2_id', type=DateTime, location='json')
        parser.add_argument('model_id', type=int, location='json')
        return parser


class StudentEnrollmentJoinedSchema(ma.SQLAlchemySchema):
    class Meta:
        course = Course
        student = Student
        student_enrollment = StudentEnrollment

    Course = fields.Nested(CourseSchema)
    Student = fields.Nested(StudentSchema)
    StudentEnrollment = fields.Nested(StudentEnrollmentSchema)