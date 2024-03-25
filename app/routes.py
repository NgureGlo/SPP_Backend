from flask import flash, request, jsonify
from flask import Flask
import urllib.parse
from app import app, db, loaded_model
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import Bcrypt
from app.models import User
from app.models import Course
from app.models import Student, Predictions
from sqlalchemy import exc, and_
import json


@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'message': 'welcome to flask app' })


# define endpoints for registering an admin
@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    data = request.json

    name = str(data['name'])
    reg_no = str(data['reg_no'])
    email = str(data['email'])
    password = str(data['password'])

    # Check if the email is valid
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        
        return jsonify({'message': 'Invalid email address.'})

    # Check password length
    if len(password) < 6:
        
        return jsonify({'message': 'Password must be at least 6 characters long.'})
    
    bcrypt = Bcrypt()

    try:

        user = User(role='Administrator', name=name, reg_no=reg_no, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Your account has been created.'})

    except Exception as e:
        return jsonify({'error': str(e)}) 


# define endpoints for registering an educator
@app.route('/register_educator', methods=['GET', 'POST'])
def register_educator():
    data = request.json

    
    name = str(data['name'])
    reg_no = str(data['reg_no'])
    email = str(data['email'])
    password = str(data['password'])

    # Check if the email is valid
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        
        return jsonify({'message': 'Invalid email address.'})

    # Check password length
    if len(password) < 6:
        
        return jsonify({'message': 'Password must be at least 6 characters long.'})
    
    bcrypt = Bcrypt()

    try:

        user = User(role='Educator', name=name, reg_no=reg_no, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Your account has been created.'})

    except Exception as e:
        return jsonify({'error': str(e)}) 


# define endpoints for registering a student
@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    data = request.json

    
    name = str(data['name'])
    reg_no = str(data['reg_no'])
    email = str(data['email'])
    password = str(data['password'])

    # Check if the email is valid
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        
        return jsonify({'message': 'Invalid email address.'})

    # Check password length
    if len(password) < 6:
        
        return jsonify({'message': 'Password must be at least 6 characters long.'})
    
    bcrypt = Bcrypt()

    try:

        user = User(role='Student', name=name, reg_no=reg_no, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Your account has been created.'})

    except Exception as e:
        return jsonify({'error': str(e)}) 


# define endpoints for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json

    email = str(data['email'])
    password = str(data['password'])

    user = User.query.filter_by(email=email).first()
    print(str(user.password))

    bcrypt = Bcrypt()

    if user and bcrypt.check_password_hash(user.password, password):
            # Login successful, redirect to dashboard or home page
            auth_result = {'uid': user.id, 'role': str(user.role.value)}
           
            return jsonify({'meessage': 'Login successful!', 'data' : auth_result})
    else:
            # Login failed, show error message
            return jsonify({'message': 'Invalid email or password.'})


# define endpoints for viewing users
@app.route('/view_users', methods=['GET'])
def view_user():
    user= User.query.all()
    user_json = [User.serialize(record) for record in user]
    return jsonify({'data': user_json})


# define endpoints for viewing a specific user
@app.route('/view_user/<int:user_id>', methods=['GET'])
def view_specificuser(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'id':user.id,
                'name': user.name,
                'email': user.email
                # Add other fields as needed
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except exc.SQLAlchemyError as e:

        return jsonify({'error': str(e)}), 500


# define endpoints for deleting a user
@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Query the user to delete
    user = User.query.get_or_404(user_id)

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    # message to confirm deletion
    return jsonify ({'message': 'User deleted successfully!'})


# define endpoints for updating a user
@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    data = request.json

    # Query the user to find user
    user = User.query.get_or_404(user_id)

    name = str(data['name'])
    photo = str(data['photo'])

    user.name=name
    user.photo=photo

    try:
        db.session.commit()

        return jsonify ({'message': 'Updated successfully!'})
    
    
    except Exception as e:
        return jsonify({'error': str(e)})
    

# define endpoints for viewing all courses
@app.route('/courses', methods=['GET'])
def courses():
    courses = Course.query.all()
    courses_json = [Course.serialize(record) for record in courses]
    return jsonify({'data': courses_json})


# define endpoints for viewing courses added by a specific lecturer
@app.route('/lecturer_courses/<int:user_id>', methods=['GET'])
def lecturer_courses(user_id):
    courses = Course.query.filter(Course.added_by == user_id)
    courses_json = [Course.serialize(record) for record in courses]
    return jsonify({'data': courses_json})



# define endpoints for adding a course
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    data = request.json

    course_code = str(data['course_code'])
    course_level = str(data['course_level'])
    course_name = str(data['course_name'])
    current_user_id = int(data['current_user_id'])
    
    if course_code and course_level and course_name:
        added_by = current_user_id  # Assuming current_user is the logged-in user
        course = Course(course_code=course_code, course_level=course_level, course_name=course_name, added_by=added_by)
        db.session.add(course)
        db.session.commit()

        return jsonify ({'message': 'Course added successfully!'})
    
    else:

        return jsonify({'message': 'Unable to add course. Please fill in all sections.'})


# define endpoints for deleting a course
@app.route('/courses/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    # Query the course to delete
    course = Course.query.get_or_404(course_id)

    # Delete the course from the database
    db.session.delete(course)
    db.session.commit()

    # message to confirm deletion
    return jsonify ({'message': 'Course deleted successfully!'})


# # Define endpoint for adding a student to a course
# @app.route('/add_student_to_course/<int:student_id>/<int:course_id>', methods=['POST'])
# def add_student_to_course(student_id, course_id):
#     try:
#         # Check if the student exists in the system
#         student = Student.query.get(student_id)
#         if not student:
#             return jsonify({'error': 'Student not found'}), 404
        
#         # Check if the course exists in the system
#         course = Course.query.get(course_id)
#         if not course:
#             return jsonify({'error': 'Course not found'}), 404
        
#         # Add the student to the course
#         course.students.append(student)
#         db.session.commit()

#         return jsonify({'message': 'Student added to course successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



# define endpoints for adding a student to a course
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json

    # Extract reg_no and course_code from request data
    reg_no = data.get('reg_no')
    course_code = data.get('course_code')

    if not reg_no or not course_code:
        return jsonify({'message': 'Please provide registration number and course code'}), 400
    
    # Check if the course exists
    course = Course.query.filter_by(course_code=course_code).first()
    if not course:
        return jsonify({'message': 'Course not in records'}), 404

    # Check if the student exists
    student = User.query.filter_by(reg_no=reg_no).first()
    if not student:
        return jsonify({'message': 'Student not in records'}), 404

    # Check if course connection already exists
    student = Student.query.filter(and_(Student.reg_no == reg_no, Student.course_code == course_code)).first()
    if student:
        return jsonify({'message': 'The student is already enrolled in this course.'})

    # Add student to the course
    if reg_no and course_code:
        student = Student(reg_no=reg_no, course_code=course_code)
        db.session.add(student)
        db.session.commit()
        return jsonify ({'message': 'Student added successfully!'})
    else:
        return jsonify({'message': 'Unable to add Student. Please fill in all sections.'})


# define endpoints for viewing all students
@app.route('/view_students', methods=['GET'])
def view_students():
    student = User.query.filter(User.role == 'Student')
    student_json = [User.serialize(record) for record in student]
    return jsonify({'data': student_json})


# define endpoints for viewing a specific student
@app.route('/view_student/<int:user_id>', methods=['GET'])
def view_specificstudent(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify(User.serialize(user)), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except exc.SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500    

    
# define endpoints for viewing a student added by a specific lecturer
@app.route('/lecturer_students/<int:lecturer_id>', methods=['GET'])
def lecturer_students(lecturer_id):
    courses = Course.query.filter(Course.added_by == lecturer_id)
    students = []

    for course in courses:
        connections = Student.query.filter(Student.course_code == course.course_code)
        for connection in connections:
            users = User.query.filter(User.reg_no == connection.reg_no)
            studs = [User.serialize(record) for record in users]
            students += studs

    unique_objects = set(json.dumps(obj, sort_keys=True) for obj in students)
    unique_students = [json.loads(obj) for obj in unique_objects]

    return jsonify({'data': unique_students})


# Define endpoints for deleting a student from a course
@app.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        # Query the student to delete
        student = Student.query.get(student_id)

        if student:
            # Delete the student from the database
            db.session.delete(student)
            db.session.commit()

            # Message to confirm deletion
            return jsonify({'message': 'Student deleted successfully!'}), 200
        else:
            # If the student is not found, return an error message
            return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        # If there is an error, return an error message
        return jsonify({'error': str(e)}), 500


# define endpoints for viewing a student from a specific courses
@app.route('/course_students/<string:course_code>', methods=['GET'])
def course_students(course_code):
    student= Student.query.filter(Student.course_code == course_code)
    student_json = [Student.serialize(record) for record in student]
    return jsonify({'data': student_json})



# define endpoints for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try: 
        # input data
        data = request.json

        reg_no = str(data['reg_no'])
        course_code = str(data['course_code'])
        assignments_viewed = 0
        assignments_submitted = 0
        quiz_started = 0
        quiz_submitted = 0
        quiz_reviewed = 0
        quiz_viewed = 0
        forums_viewed = 0
        page_views = 0
        resources_viewed = 0
        cat_1 = float(data['cat_1'])
        cat_2 = float(data['cat_2'])
        assignment = float(data['assignment'])
        project = float(data['project'])

        courses = Course.query.filter(Course.course_code == course_code)
        course_list = [Course.serialize(record) for record in courses]

        if not course_list:
            return jsonify({'message': 'Course not in records'})

        student_list = User.query.filter(User.reg_no == reg_no)

        if not student_list:
            return jsonify({'message': 'Student not in records'})
        
        connection_list = Student.query.filter(and_(Student.course_code == course_code, Student.reg_no == reg_no))
        if not connection_list:
            return jsonify({'message':'Student not registered in this course'})

        expected_exam = loaded_model.predict([[
            assignments_viewed, assignments_submitted,
            quiz_started, quiz_submitted, quiz_reviewed,
            quiz_viewed, forums_viewed, page_views,
            resources_viewed, cat_1, cat_2, assignment, project]])
        
        expected_total = cat_1 + cat_2 + assignment + project + expected_exam

        if expected_total >= 70:
            expected_grade = 'A'
        elif expected_total >= 60 and expected_total <=69:
            expected_grade = 'B'
        elif expected_total >= 50 and expected_total <=59:
            expected_grade = 'C'
        elif expected_total >= 40 and expected_total <=49:
            expected_grade = 'D'
        else:
            expected_grade = 'E'

        predictions = Predictions(reg_no=reg_no, course_code=course_code, cat_1=cat_1, cat_2=cat_2, assignment=assignment, project=project, expected_exam=expected_exam, expected_total=expected_total, expected_grade=expected_grade)
        db.session.add(predictions)
        db.session.commit()

        predictions_json = Predictions.serialize(predictions)
        return jsonify({'data': predictions_json})
        
        #return jsonify({'prediction': prediction[0][0]})
    except Exception as e:
        return jsonify({'message': str(e)})


# define endpoints for viewing all predictions
@app.route('/all_predictions', methods=['GET'])
def all_predictions():
    predictions = Predictions.query.all()
    predictions_json = [Predictions.serialize(record) for record in predictions]
    return jsonify({'data': predictions_json})


# define endpoints for viewing all predictions of a certain lecturer
@app.route('/lecturer_predictions/<int:lecturer_id>', methods=['GET'])
def lecturer_predictions(lecturer_id):
    courses = Course.query.filter(Course.added_by == lecturer_id)
    predictions = []

    for course in courses:
        pred = Predictions.query.filter(Predictions.course_code == course.course_code)
        preds = [Predictions.serialize(record) for record in pred]
        predictions += preds

    return jsonify({'data': predictions})


# define endpoints for viewing all predictions by course
@app.route('/course_predictions', methods=['GET', 'POST'])
def course_predictions():
    data = request.json
    course_code = str(data['course_code'])
    pred = Predictions.query.filter(Predictions.course_code == course_code)
    preds = [Predictions.serialize(record) for record in pred]

    return jsonify({'data': preds})


# define endpoints for viewing all predictions by student
@app.route('/student_predictions', methods=['GET', 'POST'])
def student_predictions():
    data = request.json
    reg_no = str(data['reg_no'])
    pred = Predictions.query.filter(Predictions.reg_no == reg_no)
    preds = [Predictions.serialize(record) for record in pred]
    return jsonify({'data': preds})

# define endpoints for viewing predictions by level
@app.route('/courselevel_predictions', methods=['GET', 'POST'])
def courselevel_predictions():
    data = request.json
    course_level = str(data['course_level'])
    courses = Course.query.filter(Course.course_level == course_level)
    print(courses.count())
    predictions = []

    for course in courses:
        pred = Predictions.query.filter(Predictions.course_code == course.course_code)
        preds = [Predictions.serialize(record) for record in pred]
        predictions += preds

    return jsonify({'data': predictions})

