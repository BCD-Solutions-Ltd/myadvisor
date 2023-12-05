from flask import request
from App.controllers.course import courses_Sorted_byCredits, courses_Sorted_byRating, courses_Sorted_electives_first, get_all_course_codes, get_all_courses
from App.controllers.courseHistory import getCompletedCourseCodes
from App.models import CoursePlan, Course, Student, Program
from App.database import db 
from App.controllers import program
from App.controllers import (
    get_program_by_id, 
    get_course_by_courseCode, 
    get_credits, 
    getPrereqCodes,
    
    
)
from App.models.courseHistory import CourseHistory

def convertToList(iterable):
    return list(iterable)


def create_CoursePlan(id):
    plan = CoursePlan(id)
    db.session.add(plan)
    db.session.commit()
    return plan

def getCoursePlan(studentid):
    return CoursePlan.query.filter_by(studentId=studentid).first()

def update_course_plan(plan_id):
    course_plan = CoursePlan.query.get(plan_id)
    if course_plan:
        data = request.get_json()

        student_id = data.get('student_id')
        student = Student.query.get(student_id) if student_id else None

        strategy_type = data.get('strategy_type')
        if strategy_type:
            strategy = get_strategy_instance(strategy_type)
            course_plan.set_strategy(strategy)

        course_plan.plan_id = data.get('plan_id', course_plan.plan_id)
        course_plan.student = student

        db.session.commit()
        return {'message': 'Course Plan updated successfully', 'course_plan': course_plan.get_json()}
    else:
        return {'message': 'Course Plan not found'}, 404




def possessPrereqs(Student, course):
    preqs = getPrereqCodes(course)
    student_id = Student.id
    completed = CourseHistory.query.get(student_id)
    for course in preqs:
        if course not in completed:
            return False
    
    return True

#********(Trial and error Please Review)
def isCourseOffered(courseCode):
    # Assume 'course_code' is provided as a parameter
    course = Course.query.get(courseCode)

    if not course:
        print(f"Course with code {courseCode} not found.")
        return False

    try:
        year = int(input("Enter current year: "))
        semester = int(input("Enter current semester "))

        if course.year == year and course.semester == semester:
            print(f"{courseCode} is offered in {year}, Semester {semester}.")
            return True
        else:
            print(f"{courseCode} is not offered in {year}, Semester {semester}.")
            return False
    except ValueError:
        print("Invalid input. Please enter valid integers for year and semester.")
        return False


#********(Trial and error Please Review)
def deleteCourseFromCoursePlan(plan_id, courseCode):
    # Retrieve the CoursePlan from the database based on plan_id
    course_plan = CoursePlan.query.get(plan_id)

    if not course_plan:
        print(f"Course Plan with ID {plan_id} not found.")
        return False

    # Retrieve the Course from the database based on courseCode
    course = Course.query.get(courseCode)

    if not course:
        print(f"Course with code {courseCode} not found.")
        return False

    # Check for course  in  course plan
    if course in course_plan.courses:
        # Remove the course from the course plan
        course_plan.courses.remove(course)
        db.session.commit()
        print(f"Course {courseCode} removed from Course Plan {plan_id}.")
        return True
    else:
        print(f"Course {courseCode} is not in Course Plan {plan_id}.")
        return False


def addCourseToPlan(Student, courseCode):
    course = get_course_by_courseCode(courseCode)
    if course:
        offered = isCourseOffered(courseCode)
        if offered:
            haveAllpreqs = possessPrereqs(Student, course)
            if haveAllpreqs:
                plan = getCoursePlan(Student.id)
                if plan:
                    create_CoursePlan(plan.planId, courseCode)
                    print("Course successfully added to course plan")
                    #plan_id = plan.planID
                    #plan_id_student = students.
                    return plan
                else:
                    plan = create_CoursePlan(Student.id)
                    create_CoursePlan(plan.planId, courseCode)
                    print("Plan successfully created and Course was successfully added to course plan")
                    return plan
        else:
            print("Course is not offered")
    else:
        print("Course does not exist")


def removeCourse(Student, courseCode):
    plan=getCoursePlan(Student.id)
    if plan:
        deleteCourseFromCoursePlan(plan.planId, courseCode)

def getRemainingCourses(completed, required):
    # Check if either 'completed' or 'required' is None
    if completed is None or required is None:
        return []  # Return an empty list or handle it in a way that makes sense for your application
    
    completedCodes = []
    for c in completed:
        completedCodes.append(c.code)
    
    remainingCodes = []
    for r in required:
        remainingCodes.append(r.code)
    

    notCompleted = remainingCodes.copy()
    for a in completedCodes:
        if a in notCompleted:
            notCompleted.remove(a)

    return notCompleted


def getRemainingCore(Student):
    programme=get_program_by_id(Student.program_id)
    remaining = []

    if programme:
        #reqCore=get_allCore(programme.name)
        reqCore=program.get_core_courses(programme)
        completed = Student.course_history
        remaining=getRemainingCourses(completed,reqCore)
    
    return remaining


def getRemainingFoun(Student):
    programme = get_program_by_id(Student.program_id)
    remaining =[]

    if programme:
        #reqFoun = get_allFoun(programme.name)
        reqFoun = program.get_foun_courses(programme)
        completed = Student.course_history
        remaining=getRemainingCourses(completed,reqFoun)
    
    return remaining


def getRemainingElec(Student):
    programme = get_program_by_id(Student.program_id)  # Get the student's program
    remaining = []

    if programme:
        #reqElec = get_allElectives(programme.name)  # Use the instance method to get elective courses
        reqElec = program.get_elective_courses(programme)
        completed = Student.course_history
        remaining = getRemainingCourses(completed, reqElec)
            
    return remaining


def remElecCredits(Student):
    programme = get_program_by_id(Student.program_id)  # Get the student's program
    completedcourses = Student.course_history
    requiredCreds = 0
    type = 'elec'

    if programme:
        requiredCreds = programme.elective_credits  # Access the elective_credits attribute
        courses = get_all_courses(program)  # Use the instance method to get elective courses
        elective_courses = program.get_all_courses_by_type(type)
        electCodes = convertToList(elective_courses)
        if electCodes:
            for code in electCodes:
                if code in completedcourses:
                    c = get_course_by_courseCode(code)  # Get course
                    if c:
                        requiredCreds = requiredCreds - c.credits  # Subtract credits       
    return requiredCreds





def findAvailable(courseList):
    listing= get_all_course_codes()
    available=[]

    for code in courseList:
        if code in listing:
            available.append(code)

    return available        #returns an array of course codes


def checkPrereq(Student, recommnded):
    validCourses=[]
    for course in recommnded:
        c = get_course_by_courseCode(course)
        satisfied = possessPrereqs(Student, c)
        if satisfied:
            validCourses.append(c.courseCode)
    
    return validCourses

def getTopfive(list):
    return list[:5]

#def PrioritizeElectivesStrategy(Student):
    program = get_program_by_id(Student.program_id)
    completed = Student.course_history
    codesSortedbyelectives = program.programCourses_SortedbyElectivesFirst(Student.program_id)
    type = 'elec'
    coursesToDo = removeCoursesFromList(completed, codesSortedbyelectives)
    elecCredits = remElecCredits(Student)
    
    if elecCredits == 0:
        allElectives = program.get_all_courses_by_type(type)
        coursesToDo = removeCoursesFromList(allElectives, coursesToDo)
    
    coursesToDo = findAvailable(coursesToDo)

    ableToDo = checkPrereq(Student, coursesToDo)
    
    
    return getTopfive(ableToDo)

#def PrioritizeElectivesStrategy(Student):
    #get available electives
    electives=findAvailable(getRemainingElec(Student))      
    credits=remElecCredits(Student)
    courses=[]
    
    #select courses to satisfy the programme's credit requirements
    for c in electives:     
        if credits>0:
            courses.append(c)
            credits = credits - get_credits(c)
    
    #merge available, required core and foundation courses
    courses = courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))

    courses = checkPrereq(Student,courses)
    return getTopfive(courses)


def removeCoursesFromList(list1,list2):
    newlist = list2.copy()
    for a in list1:
        if a in newlist:
            newlist.remove(a)
    return newlist
    

def EasyCoursesStrategy(Student):
    #program = get_program_by_id(Student.program_id)
    student_id = Student.id
    completed = getCompletedCourseCodes(student_id)
    codesSortedbyRating = courses_Sorted_byRating()
    
    coursesToDo = removeCoursesFromList(completed, codesSortedbyRating)
    top_five_courses =getTopfive(coursesToDo)
    #for course_code in top_five_courses:
        #course = Course.query.filter_by(courseCode=course_c0de).first()
        #addCourseToPlan(student_id, course_code)

    return top_five_courses
    
   
    return getTopfive(coursesToDo)


def PrioritizeElectivesStrategy(Student):
    sortedCourses = courses_Sorted_electives_first()

    student_id = Student.id
    completed = getCompletedCourseCodes(student_id)
    coursesToDo = removeCoursesFromList(completed, sortedCourses)
    
    #coursesToDo = findAvailable(coursesToDo)
    #ableToDo = checkPrereq(Student, coursesToDo)
    top_five_courses =getTopfive(coursesToDo)
    #for course_code in top_five_courses:
        #course = Course.query.filter_by(courseCode=course_c0de).first()
        #addCourseToPlan(student_id, course_code)

    return getTopfive(sortedCourses)



#def CustomPlanStrategy(Student):
    program = get_program_by_id(Student.program_id)
    completed = Student.course_history
    codesSortedbyRating = programCourses_SortedbyRating(Student.program_id)

    coursesToDo = removeCoursesFromList(completed, codesSortedbyRating)
    elecCredits = remElecCredits(Student)
    
    if elecCredits == 0:
        allElectives = convertToList(get_allElectives(program.name))
        coursesToDo = removeCoursesFromList(allElectives, coursesToDo)
    
    coursesToDo = findAvailable(coursesToDo)

    ableToDo = checkPrereq(Student, coursesToDo)
    
    
    return getTopfive(ableToDo)

#********(Trial and error Please Review)
def CustomPlanStrategy(Student):
    student = Student.query.get(id)
    
    if not student:
        return {'message': f'Student with ID {id} not found.'}, 404


    try:
        semester = int(input("Enter your semester: "))
    except ValueError:
        return {'message': 'Invalid input. Please enter a valid semester number.'}, 400

    # Get a list of available courses for the current semester
    available_courses = Course.query.filter_by(semester=semester).all()

    if not available_courses:
        return {'message': f'No courses available for semester {semester}.'}, 400

    # Let the student choose 5 courses
    chosen_courses = []
    for i in range(5):
        print(f"Choose course {i + 1} from the available courses:")
        print("Available Courses:")
        for j, course in enumerate(available_courses, start=1):
            print(f"{j}. {course.courseCode} - {course.courseTitle}")

        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(available_courses):
                chosen_course = available_courses[choice - 1]
                chosen_courses.append(chosen_course)
                #addCourseToPlan(student, chosen_course)
                available_courses.remove(chosen_course)
            else:
                print("Invalid choice. Please enter a valid number.")
                i -= 1
        
        except ValueError:
            print("Invalid input. Please enter a number.")
        
        
   



def FastGradStrategy(Student):
    #program = get_program_by_id(Student.program_id)
    sortedCourses = courses_Sorted_byCredits()

    student_id = Student.id
    completed = getCompletedCourseCodes(student_id)
    coursesToDo = removeCoursesFromList(completed, sortedCourses)
    
    #coursesToDo = findAvailable(coursesToDo)
    #ableToDo = checkPrereq(Student, coursesToDo)
    top_five_courses =getTopfive(coursesToDo)

    #for course_code in top_five_courses:
        #course = Course.query.filter_by(courseCode=course_c0de).first()
        #addCourseToPlan(student_id, course_code)

    return getTopfive(coursesToDo)

#def commandCall(Student, command):
    courses = []

    if command == "electives":
        courses = prioritizeElectives(Student)
    
    elif command == "easy":
        courses = easyCourses(Student)
    
    elif command == "fastest":
        courses = fastestGraduation(Student)
    
    else:
        print("Invalid command")
    
    return courses

#********(Trial and error Please Review)
def get_strategy_instance(strategy_type):
    if strategy_type == 'customplan':
        return CustomPlanStrategy(Student)
    elif strategy_type == 'fastgrad':
        return FastGradStrategy(Student)
    elif strategy_type == 'easycourses':
        return EasyCoursesStrategy(Student)
    elif strategy_type == 'prioritizeelectives':
        return PrioritizeElectivesStrategy(Student)
    else:
        # Default to CustomPlanStrategy if the strategy_type is not recognized
        return CustomPlanStrategy(Student)


#def generator(Student, command):
    courses = []

    plan = getCoursePlan(Student.id)

    if plan is None:
        plan = plan = create_CoursePlan(Student.id)

    
    courses = commandCall(Student, command)

    existingPlanCourses = get_all_courses_by_planid(plan.planId)


    planCourses = []
    for q in existingPlanCourses:
        planCourses.append(q.code)

    for c in courses: 
        if c not in planCourses:
            create_CoursePlan(plan.planId, c)

    return courses
    for c in courses: 
        if c not in planCourses:
            createPlanCourse(plan.planId, c)

    return courses
