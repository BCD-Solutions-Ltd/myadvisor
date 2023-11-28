from App.database import db
from App.models import department

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    core_credits = db.Column(db.Integer)
    elective_credits = db.Column(db.Integer)
    foun_credits = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    dept = db.relationship('Department', back_populates='prog')
    stu = db.relationship('Student', back_populates='prog', uselist=False)
    
    courses = db.relationship('Course', backref='program', lazy=True)


    def __init__(self, name, core, elect, foun):
       self.name = name
       self.core_credits = core
       self.elective_credits = elect
       self.foun_credits = foun


    def get_json(self):
        return{
            'Program ID:': self.id,
            'Department ID: ': self.department_id,
            'Program Name: ': self.name,
            'Core Credits: ': self.core_credits,
            'Elective Credits ': self.elective_credits,
            'Foundation Credits: ': self.foun_credits
        }
       