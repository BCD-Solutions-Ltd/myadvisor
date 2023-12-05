from App.models import User  
from App.database import db

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.String(10), db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(50))
    gpa = db.Column(db.Float) 
    program_id = db.Column(db.ForeignKey('programs.id')) 
    
    prog = db.relationship('Program', back_populates='students')
    #course_plans = db.relationship('CoursePlan', back_populates='student', uselist=True)
    course_plan = db.relationship('CoursePlan', back_populates= 'students', uselist=False)
    
    

    def __init__(self, name, password, program_id):
        super().__init__(name, password)
        self.id = super().id
        self.name = name
        self.gpa= 0.0
        self.program_id = program_id

    def get_json(self):
        return{'Student ID': self.id,
            'Name': self.name,
            'Program' : self.program_id,
            'GPA: ' : self.gpa
            
        }



