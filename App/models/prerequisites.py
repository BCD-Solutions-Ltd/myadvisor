from App.database import db
class Prerequisites(db.Model):

    prereq_code = db.Column(db.String, primary_key=True)
    courseCode = db.Column(db.String(8), db.ForeignKey('courses.id'))
    

    def __init__(self, prereq_code, nameofCourse):
        self.prereq_courseCode = prereq_code


    def get_json(self):
        return{
            'Prerequisite Code': self.prereq_courseCode,
        } 
