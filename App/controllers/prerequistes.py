from App.models import Prerequisites
from App.database import db
from App.models.course import Course

def create_prereq(prereqCode, courseCode):
    prereq = Prerequisites(prereqCode, courseCode)
    db.session.add(prereq)
    db.session.commit()

#def get_all_prerequisites(courseCode):
    #course = courseCode
    #prereq = course.prereq
    #return prereq

def get_all_prerequisites( courseCode):
    

    course = Course.query.get(courseCode)

    if course:
        prerequisites = course.prereq  # Accessing the prereq attribute
        return prerequisites
    else:
        return None



def getPrereqCodes(courseCode):
    prereqs = get_all_prerequisites(courseCode)
    codes = prereqs

    
    return codes
