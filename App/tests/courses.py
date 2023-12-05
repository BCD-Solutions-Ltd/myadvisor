import pytest, unittest
from App.models import Course, Prerequisites, prerequisites
from App.controllers import create_course, courses_Sorted_byRating_Objects, get_course_by_courseCode, create_prereq, getPrereqCodes
from App.main import create_app
from App.database import db, create_db

class CourseUnitTests(unittest.TestCase):

    def test_new_course(self):
        courseCode = "INFO2605"
        courseName = "Professional Ethics and Law"
        credits = 3
        rating = 4 
        type = "core"
        grade = ""
        semester= "1"
        year = "2"
        complete = "true"

        course = Course(courseCode, courseName, credits,rating, type, grade, semester, year, complete )

        self.assertEqual(course.courseCode, courseCode)
        self.assertEqual(course.courseName, courseName)
        self.assertEqual(course.credits, credits)
        self.assertEqual(course.rating, rating)
        self.assertEqual(course.type, type)
        self.assertEqual(course.grade, grade) 
        self.assertEqual(course.semester, semester)
        self.assertEqual(course.year, year)
        self.assertEqual(course.complete, complete)               

    def test_course_json(self):
        courseCode = "INFO2605"
        courseName = "Professional Ethics and Law"
        credits = 3
        rating = 4 
        type = "core"
        grade = ""
        semester= "1"
        year = "2"
        complete = "true"

        course = Course(courseCode, courseName, credits,rating, type, grade, semester, year, complete )
        course_json = course.get_json()

        self.assertDictEqual(course_json, {
            'Course Code:': self.id,
            'Course Name: ': self.courseTitle,
            'Course Grade: ': self.grade,
            'No. of Credits: ': self.credits,
            'Course Type: ': self.type,
            'course rating': self.rating,
            'Semester: ': self.semester,
            'Year: ': self.year,
            'Completed?': self.complete,
            'Prerequisites: ': [prerequisites.get_json() for prerequisite in self.prerequisites]
            })


    def test_new_prerequisite(self):
        prereq=Prerequisites("INFO2605","Introduction to Information Technology Concepts")
        assert prereq.prereq_courseCode=="INFO2605"

    def test_prerequisite_toJSON(self):
        prereq=Prerequisites("INFO2605","Introduction to Information Technology Concepts")
        prereq_json=prereq.get_json()
        self.assertDictEqual(prereq_json,{
            'prereq_id': None, 
            'prerequisite_courseCode': 'INFO2605', 
            'prerequisite_course': 'Introduction to Information Technology Concepts'
            })
    

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

def test_create_course():
    courseCode = "INFO2605"
    courseName = "Professional Ethics and Law"
    credits = 3
    rating = 4 
    type = "core"
    grade = ""
    semester= "1"
    year = "2"
    complete = "true"
    prereqs=[]

    course = create_course(courseCode, courseName, credits, rating, type, grade, semester, year, complete  , prereqs)

    assert get_course_by_courseCode("INFO2605") != None


class CourseIntegrationTests(unittest.TestCase):    
    def test_courses_sorted_by_rating(self):
        prereqs=[]

        create_course_new("COMP3605","Data Analytics","1","4","elec","","2","3","","COMP2611","")
        create_course_new("COMP3610","Big Data Analytics","6","5","elec","","1","3","","COMP3605","")
        create_course_new("COMP3611","Small Data Analytics","1","1","elec","","1","3","","COMP2611","")
        sortedCourses = courses_Sorted_byRating_Objects()

        self.assertTrue(sortedCourses)

        for i in range(len(sortedCourses) - 1):
            self.assertLessEqual(sortedCourses[i].rating, sortedCourses[i + 1].rating)


    def test_create_prerequisite(self):
        create_course_new("MATH2250","Industrial Statistics","3","2","elec","","","2","","","")
        code = MATH2250
        prereqcode = Math1115
        addprereqCourses( code, prereqcode)
        
