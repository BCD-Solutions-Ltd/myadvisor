from flask import request
from sqlalchemy import desc
from App.models import Course, Prerequisites, Semester
from App.controllers import prerequistes, semester
from App.database import db
import json, csv

from App.models.program import Program

#def createPrerequistes(prereqs, courseName):
 ##      prereq_course = Course.query.filter_by(courseCode=prereq_code).first()
        
   #     if prereq_course:
    #        create_prereq(prereq_code,courseName) 

def create_course():
    data = request.get_json()
    prereq_id = data.get('prereq_id')  
    prereq_id = Prerequisites.query.get(prereq_id) if prereq_id else None
    semester_id = int(data['semester_id'])


    new_course = Course(
        id=data['id'],
        courseTitle=data['courseTitle'],
        complete=bool(data['complete']),
        credits=int(data['credits']),
        type= (data['type']),
        rating= int(data['rating']),
        grade=float(data['grade']), 
        semester_id = semester_id,
        year=int(data['year']),
        prereq_id = prereq_id,
        course_plan_id=int(data['course_plan_id'])
    )

    db.session.add(new_course)
    db.session.commit()
    return "Course created successfully", 201

def create_course_new(id,courseTitle,credits,rating,type, grade , semester_id ,year ,complete,prereq_id ,course_plan_id ):
    course = Course.query.get(id)
    if course:
        return None
    new_course = Course(id,courseTitle,credits,rating,type, grade , semester_id ,year ,complete,prereq_id ,course_plan_id )
    db.session.add(new_course)
    db.session.commit()
    return new_course

   

def createCoursesfromFile(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                courseCode = row["courseCode"]
                courseTitle = row["courseTitle"]
                credits = int(row["numCredits"])
                rating = int(row["rating"])
                type = row['type']
                grade=row['grade']
                semester=row['semester']
                year=int (row['year'])
                complete= row['complete']
                prereq= row["preReqs"].split(',')

                create_course(courseCode, courseTitle, credits,rating, grade, semester, year, complete, prereq)
                
    except FileNotFoundError:
        print("File not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    print("Courses added successfully.")
    
def get_course_by_courseCode(code):
    return Course.query.filter_by(id=code).first()

def get_all_course_codes():
    try:
        course_codes = Course.query.with_entities(Course.id).all()
        if course_codes:
            return [code[0] for code in course_codes]
        else:
            raise ValueError("No course codes found.")
    except Exception as e:
        print(f"Error: {e}")
        return None

def add_prereq_to_course(code, prereq_code):
    course = Course.query.filter_by(id=code).first()
    if course:
            course.prereq = prereq_code
            db.session.commit()
            return course

#def addSemesterCourses( code, semester):
        #course = Course.query.filter_by(id=code).first()

        #if course:
        #    course.semester = semester
         #   db.session.commit()
         #   return course
       # else:
           # return {"message": "Course not found"},


def courses_Sorted_byRating():
    courses =  Course.query.order_by(Course.rating.asc()).all()
    codes = []

    for c in courses:
        codes.append(c.id)
    
    return codes



def courses_Sorted_byCredits():
    courses = Course.query.order_by(desc(Course.credits)).all()
    codes = []

    for c in courses:
        codes.append(c.id)
    
    return codes

def courses_Sorted_electives_first():
    courses = Course.query.filter_by(type='elec').order_by(Course.rating.asc()).all()
    codes = []

    for c in courses:
        codes.append(c.id)
    
    return codes


def courses_Sorted_byRating_Objects():
    return Course.query.order_by(Course.rating.asc()).all()


    

def get_prerequisites(code):
    course = get_course_by_courseCode(code)
    prereqs = prerequistes.get_all_prerequisites(code)
    return prereqs

def get_credits(code):
    course = get_course_by_courseCode(code)
    return course.credits if course else 0

def get_ratings(code):
    course = get_course_by_courseCode(code)
    return course.rating if course else 0

def get_all_courses_new():
    return Course.query.all()

def get_all_courses_new_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses_json = [course.get_json() for course in courses]
    return courses_json

def get_all_courses():
    courses = Course.query.all()
    course_list = []
    for course in courses:
        course_data = {
            "id": course.id,
            "courseTitle": course.courseTitle,
            "complete": course.complete,
            "credits": course.credits,
            "grade": course.grade,
            "semester": course.semester,
            "year": course.year,
            "course_plan_id": course.course_plan_id
        }
        course_list.append(course_data)
    return {"courses": course_list}


def get_course(course_id):
    course = Course.query.get(course_id)
    if course:
        course_data = {
            "id": course.id,
            "courseTitle": course.courseTitle,
            "complete": course.complete,
            "credits": course.credits,
            "grade": course.grade,
            "semester": course.semester,
            "year": course.year,
            "course_plan_id": course.course_plan_id
        }
        return course_data
    else:
        return {"message": "Course not found"}, 404
    

def addSemesterCourses( code, semester):
        course = Course.query.filter_by(id=code).first()

        if course:
            course.semester = semester
            db.session.commit()
            return course
        else:
            return {"message": "Course not found"},

def addprereqCourses( code, prereqcode):
        course = Course.query.filter_by(id=code).first()

        if course:
            course.prereq = prereqcode
            db.session.commit()
            return course
        else:
            return {"message": "Course not found"},

def getAllCourses(semester_id):
        
        courses = Course.query.filter_by(semester=semester_id).all()
        course_ids = [course.id for course in courses]
        return course_ids


def get_course_codes_by_semester(self, programname, semester):
        program = Program.query.filter_by(name=programname).first()

        if program:
            # Assuming you have a relationship between Program and Course, adjust as needed
            courses = Course.query.filter_by(course_plan_id=program.id, semester=semester).all()

            # Extracting course codes
            course_codes = [course.id for course in courses]
            return course_codes
        else:
            return None


def update_course(course_code):
    course = Course.query.get(course_code)
    if course:
        data = request.get_json()
        prereq_id = data.get('prereq_id')
        prereq = Prerequisites.query.get(prereq_id) if prereq_id else None

        course.title = data.get('courseTitle', course.title)
        course.credits = data.get('credits', course.credits)
        course.grade = data.get('grade', course.grade)
        course.semester = data.get('semester', course.semester)
        course.year = data.get('year', course.year)
        course.complete = data.get('complete', course.complete)
        course.prereq = prereq

        db.session.commit()
        return {'message': 'Course updated successfully', 'course': course.get_json()}
    else:
        return {'message': 'Course not found'}, 404


def delete_course(course_code):
    course = Course.query.get(course_code)
    if course:
        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted successfully'}, 200
    else:
        return {'message': 'Course not found'}, 404


















