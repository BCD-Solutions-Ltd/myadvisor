from App.database import db
from App.models import Student
from App.models import Course

class StudentCourse(db.Model):
    __tablename__='student_course'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    #course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
