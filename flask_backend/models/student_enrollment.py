from flask_restful import reqparse, inputs
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
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.Integer, db.ForeignKey("course.course_number"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)



class StudentEnrollmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StudentEnrollment

    id = fields.Integer()
    course_number = fields.Integer()
    student_id = fields.Integer()

    @post_load
    def make_model(self, data, **kwargs):
        return StudentEnrollment(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('course_number', type=int, location='json')
        parser.add_argument('student_id', type=int, location='json')
        return parser


class StudentEnrollmentJoinedSchema(ma.SQLAlchemySchema):
    class Meta:
        course = Course
        student = Student
        student_enrollment = StudentEnrollment

    Course = fields.Nested(CourseSchema)
    Student = fields.Nested(StudentSchema)
    StudentEnrollment = fields.Nested(StudentEnrollmentSchema)