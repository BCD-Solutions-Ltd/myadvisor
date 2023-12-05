from App.database import db 
from flask import jsonify
from App.models import CourseHistory  

def create_course_history(course_id, student_id, grade):
    new_course_history = CourseHistory(course_id=course_id, student_id=student_id, grade=grade)
    db.session.add(new_course_history)
    db.session.commit()
    return jsonify({'message': 'Course history created successfully'})

def get_course_history(course_history_id):
    course_history = CourseHistory.query.get(course_history_id)
    if course_history:
        return jsonify({'course_history': course_history.serialize()})
    else:
        return jsonify({'message': 'Course history not found'}), 404

def update_course_history(course_history_id, new_course_id, new_student_id):
    course_history = CourseHistory.query.get(course_history_id)
    if course_history:
        course_history.course_id = new_course_id
        course_history.student_id = new_student_id
        db.session.commit()
        return jsonify({'message': 'Course history updated successfully'})
    else:
        return jsonify({'message': 'Course history not found'}), 404

def add_course_to_course_history(student_id, course_id, grade):
    # Check if the course is already in the CourseHistory for the student
    existing_entry = CourseHistory.query.filter_by(student_id=student_id, course_id=course_id).first()

    if existing_entry:
        return jsonify({'message': 'Course already exists in the student\'s CourseHistory'}), 400

    # Create a new entry in the CourseHistory
    new_course_history_entry = CourseHistory(
        student_id=student_id,
        course_id=course_id,
        grade=grade   
    ) 
    return jsonify({'message': 'Course {course_id} with Grade {grade} added to student with id {student_id}'})


def getCompletedCourseCodes(student_id):
    completed_courses = CourseHistory.query.filter_by(student_id=student_id).all()

    course_ids = [course.course_id for course in completed_courses]

    return course_ids, 200

def getCompletedCourseCodesAndGrade(student_id):
    completed_courses = CourseHistory.query.filter_by(student_id=student_id).all()

    courses_data = []

    for course in completed_courses:
        course_data = {
            'course_id': course.course_id,
            'grade': course.grade  # Assuming there's a 'grade' attribute in your CourseHistory model
        }
        courses_data.append(course_data)

    return jsonify({'courses_and_grades': courses_data}), 200

def delete_course_history(course_history_id):
    course_history = CourseHistory.query.get(course_history_id)
    if course_history:
        db.session.delete(course_history)
        db.session.commit()
        return jsonify({'message': 'Course history deleted successfully'})
    else:
        return jsonify({'message': 'Course history not found'}), 404
