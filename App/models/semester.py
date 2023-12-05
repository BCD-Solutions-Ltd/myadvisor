from App.database import db


class Semester(db.Model):
    __tablename__ = 'semesters'
    id = db.Column(db.Integer, primary_key=True)
    semester_title = db.Column(db.String(2))

    course_plans = db.relationship('CoursePlan', backref='semesters', lazy=True)

    def __init__(self, sem_id, sem_title):
        self.id = sem_id
        self.semester_title = sem_title
        

        
        
