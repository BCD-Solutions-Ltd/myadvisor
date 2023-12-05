from flask import Blueprint, request, jsonify
from App.database import db
from App.models import Semester


def get_semesters():
    semesters = Semester.query.all()
    semesters_list = [
        {'id': semester.id, 'semester_title': semester.semester_title}
        for semester in semesters
    ]
    return jsonify({'semesters': semesters_list})


def get_semester(semester_id):
    semester = Semester.query.get(semester_id)
    if semester:
        return jsonify({'id': semester.id, 'semester_title': semester.semester_title})
    else:
        return jsonify({'error': 'Semester not found'}), 404
    
def get_semester_title (semester_id):
    semester = Semester.query.get(semester_id)
    if semester:
        return semester.semester_title



def create_semester():
    data = request.get_json()
    semester_title = data.get('semester_title')
    semester_id = data.get('semester_id')

    new_semester = Semester(semester_id=semester_id, semester_title=semester_title)

    db.session.add(new_semester)
    db.session.commit()

    return jsonify({'message': 'Semester created successfully'}), 201


def update_semester(semester_id):
    semester = Semester.query.get(semester_id)
    if not semester:
        return jsonify({'error': 'Semester not found'}), 404

    data = request.get_json()
    semester.semester_title = data.get('semester_title', semester.semester_title)

    db.session.commit()

    return jsonify({'message': 'Semester updated successfully'})


def delete_semester(semester_id):
    semester = Semester.query.get(semester_id)
    if not semester:
        return jsonify({'error': 'Semester not found'}), 404

    db.session.delete(semester)
    db.session.commit()

    return jsonify({'message': 'Semester deleted successfully'})

