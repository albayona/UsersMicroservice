# =============================================================================
# File name: user_model.py
# Author: Andy Ortiz
# Date created: 11/17/2020
# Date last modified: 11/17/2020
# Python Version: 3.8.5
# =============================================================================

# =============================================================================
# Imports
# =============================================================================

from db import db
from bkrypt import bcrypt

class UserModel(db.Model):
    __tablename__ = 'booklick_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    code = db.Column(db.Integer)
    booklists = db.relationship("BooklistModel")
    role = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'booklick_user',
        'polymorphic_on': role
    }

    @classmethod
    def find_by_username(cls, username):
        # we can concatenate filter_by's or add each filter separated by a comma
        # SELECT * FROM items WHERE name=name LIMIT 1 (returns ItemModel object)
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        # session is a collection of objects we can write to the db
        db.session.add(self)  # will also update
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class AdminModel(UserModel):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    picture = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def _init_(self, username: str, email: str, code: int, first_name: str, last_name: str,
               password: str, description: str, picture: str):


    def json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'username': self.username, 'email': self.email, 'code': self.code,
                'description': self.description, 'picture': self.picture}

class ProfessorModel(UserModel):
    professor_courses_table = db.Table('professor_courses', db.Model.metadata,
                                       db.Column('professor_id', db.Integer,
                                                 db.ForeignKey('professor.id')),
                                       db.Column('course_id', db.Integer,
                                                 db.ForeignKey('course.id'))
                                       )

    __tablename__ = 'professor'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    picture = db.Column(db.String(100))

    courses = db.relationship("CourseModel",
                              secondary=professor_courses_table,
                              backref=db.backref('professors', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'professor',
    }

    def _init_(self, username: str, email: str, code: int, first_name: str, last_name: str,
               password: str, description: str, picture: str):


    def json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'username': self.username, 'email': self.email, 'code': self.code,
                'description': self.description, 'picture': self.picture}


class StudentModel(UserModel):
    student_courses_table = db.Table('student_courses', db.Model.metadata,
                                     db.Column('student_id', db.Integer,
                                               db.ForeignKey('student.id')),
                                     db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
                                     )

    student_majors_table = db.Table('student_majors', db.Model.metadata,
                                    db.Column('student_id', db.Integer,
                                              db.ForeignKey('student.id')),
                                    db.Column('major_id', db.Integer, db.ForeignKey('major.id'))
                                    )

    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('booklick_user.id'), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    picture = db.Column(db.String(100))
    semester = db.Column(db.Integer)
    courses = db.relationship("CourseModel",
                              secondary=student_courses_table,
                              backref=db.backref('students', lazy=True))

    majors = db.relationship("MajorModel",
                             secondary=student_majors_table,
                             backref=db.backref('students', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username: str, email: str, code: int, first_name: str, last_name: str,
                 password: str, description: str, picture: str, semester: int):
        self.username = username
        self.email = email
        self.code = code
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.description = description
        self.picture = picture
        self.semester = semester

    def json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'username': self.username, 'email': self.email, 'code': self.code,
                 'description': self.description,
                'picture': self.picture, 'semester': self.semester}


