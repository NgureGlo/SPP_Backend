from app import db
from flask_bcrypt import Bcrypt
from enum import Enum
from datetime import datetime
import json
from sqlalchemy_serializer import SerializerMixin

# user table 

bcrypt = Bcrypt()

class Role(Enum):
    Administrator = 'Administrator'
    Educator = 'Educator'

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(Role), nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    photo_url = db.Column(db.String(150), nullable=True)

    def __init__(self, role, name, email, password):
        self.role = role
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def serialize(self):
        return {
            'id': self.id,
            'role': str(self.role.value),
            'name': str(self.name),
            'email': str(self.email)
        }

# add course table 

class CourseLevel(Enum):
    Level_100 = 'Level 100'
    Level_200 = 'Level 200'
    Level_300 = 'Level 300'
    Level_400 = 'Level 400'

    def __str__(self):
        return self.value


class Course(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    course_level = db.Column(db.Enum(CourseLevel), nullable=False)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    added_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    deletion_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"Course(course_level={self.course_level}, course_code={self.course_code}, course_name={self.course_name})"
    
    def serialize(self):
        return {
            'id': self.id,
            'course_level': str(self.course_level),
            'course_code': str(self.course_code),
            'course_name': str(self.course_name),
            'added_by': str(self.added_by),
            'added_date': str(self.added_date),
            'deleted_by': str(self.deleted_by),
            'deletion_date': str(self.deletion_date)
        }

# add students table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_reg_no = db.Column(db.String(20), unique=True, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'student_reg_no': str(self.student_reg_no),
            'student_name': str(self.student_name),
            'course_id': str(self.course_id)
        }