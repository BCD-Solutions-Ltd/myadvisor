from App.database import db
from App.models import prerequisites, courseHistory
import json

class Course(db.Model):
    __tablename__='courses'
    id = db.Column(db.String(8), primary_key=True)
    courseTitle = db.Column(db.String(50))
    credits = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    type = db.Column(db.String(5))
    grade = db.Column(db.String(3))
    semester = db.Column(db.Integer)
    year = db.Column(db.Integer)
    complete = db.Column(db.String(3))
    prereq = db.Column(db.String(8))
    course_plan_id = db.Column(db.Integer, db.ForeignKey('course_plans.id'), nullable=False)
    
    
    prereqq = db.relationship('Prerequisites', backref='course', lazy=True)

    
    def __init__(self, code, title, credits, ratings,  grade, type,  semester, year, complete, prereq,course_plan_id):
        self.id = code
        self.courseTitle = title
        self.credits = credits
        self.grade = grade
        self.type = type
        self.rating = ratings
        self.semester = semester
        self.year = year
        self.complete = complete
        self.prereq = prereq
        self.course_plan_id = course_plan_id
    
    def get_json(self):
        return{
            'Course Code:': self.id,
            'Course Name: ': self.courseTitle,
            'Course Grade: ': self.grade,
            'No. of Credits: ': self.credits,
            'Course Type: ': self.type,
            'course rating': self.rating,
            'Semester: ': self.semester,
            'Year: ': self.year,
            'Completed?': self.complete,
            'Prerequisites: ': self.prereq,
            'Course_plan_id':self.course_plan_id
        }
