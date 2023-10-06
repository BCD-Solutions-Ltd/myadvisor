from App.database import db 

class CoursesOfferedPerSem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.ForeignKey('course.courseCode'))
    
    associated_course = db.relationship('Course', back_populates='offered', overlaps="courses")

    def __init__(self, courseCode):
        self.offered = courseCode
       
    def get_json(self):
        return{
            'Course Code:': self.offered
        }
