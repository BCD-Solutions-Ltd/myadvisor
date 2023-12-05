from App.models import Student, CoursePlan, Program
from App.controllers import (get_program_by_name)
from App.database import db

def create_student(name, password, program):
    student = Student.query.get(name)
    if student:
        return None
    new_student = Student(name, password, program)
    db.session.add(new_student)
    db.session.commit()
    return new_student

def get_student_by_id(ID):
    return Student.query.filter_by(id=ID).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def update_student(id, username):
    student = get_student_by_id(id)
    if student:
        student.name = username
        db.session.add(student)
        db.session.commit()
        return student

def enroll_in_programme(student_id, programme_id):
    student = get_student_by_id(student_id)
    if student:
        programme = Program.query.get(programme_id)
        if programme:
            student.program_id = programme_id
            db.session.add(student)
            db.session.commit()
    return student.program_id

def verify_student(username):
    student=Student.query.filter_by(id=username).first()
    if student:
        return True
    return False



