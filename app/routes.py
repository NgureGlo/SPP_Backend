from flask import flash, request, jsonify
from app import app, db, loaded_model
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import Bcrypt
from app.models import User
from app.models import Course
from app.models import Student


@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'message': 'welcome to flask app' })

# define endpoints for registering admin
@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    data = request.json

    name = str(data['name'])
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

        user = User(role='Administrator', name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Your account has been created.'})

    except Exception as e:
        return jsonify({'error': str(e)}) 

# define endpoints for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json

    
    name = str(data['name'])
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

        user = User(role='Educator', name=name, email=email, password=password)
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
    

# define endpoints for viewing a course
@app.route('/courses', methods=['GET'])
def courses():
    courses = Course.query.all()
    courses_json = [Course.serialize(record) for record in courses]
    return jsonify({'data': courses_json})

# define endpoints for adding a course
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    data = request.json
    print (str(data))

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

# define endpoints for adding a student
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    print (str(data))

    student_reg_no = str(data['student_reg_no'])
    student_name = str(data['student_name'])
    course_id = str(data['course_id'])
    
    if student_reg_no and student_name and course_id:
        student = Student(student_reg_no=student_reg_no, student_name=student_name, course_id=course_id)
        db.session.add(student)
        db.session.commit()

        return jsonify ({'message': 'Student added successfully!'})
    
    else:

        return jsonify({'message': 'Unable to add Student. Please fill in all sections.'})
    
# define endpoints for viewing a student
@app.route('/view_students', methods=['GET'])
def view_students():
    student= Student.query.all()
    student_json = [Student.serialize(record) for record in student]
    return jsonify({'data': student_json})

# define endpoints for viewing a student added by a specific lecturer
@app.route('/lecturer_students/<int:lecturer_id>', methods=['GET'])
def lecturer_students(lecturer_id):
    student= Student.query.filter(Student.lecturer == lecturer_id)
    student_json = [Student.serialize(record) for record in student]
    return jsonify({'data': student_json})

# define endpoints for deleting a student
@app.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    # Query the student to delete
    student = Student.query.get_or_404(student_id)

    # Delete the student from the database
    db.session.delete(student)
    db.session.commit()

    # message to confirm deletion
    return jsonify ({'message': 'Student deleted successfully!'})

# define endpoints for viewing a student from a specific courses
@app.route('/course_students/<int:course_id>', methods=['GET'])
def course_students(course_id):
    student= Student.query.filter(Student.course_id == course_id)
    student_json = [Student.serialize(record) for record in student]
    return jsonify({'data': student_json})

# define endpoints for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try: 
        # input data
        data = request.json

        assignments_viewed = int(data['assignments_viewed'])
        assignments_submitted =int(data['assignments_submitted'])
        quiz_started = int(data['quiz_started'])
        quiz_submitted = int(data['quiz_submitted'])
        quiz_reviewed = int(data['quiz_reviewed'])
        quiz_viewed = int(data['quiz_viewed'])
        forums_viewed = int(data['forums_viewed'])
        page_views = int(data['page_views'])
        resources_viewed = int(data['resources_viewed'])
        quiz_1 = float(data['quiz_1'])
        quiz_2 = float(data['quiz_2'])
        assignment = float(data['assignment'])
        project = float(data['project'])

        prediction = loaded_model.predict([[
            assignments_viewed, assignments_submitted,
            quiz_started, quiz_submitted, quiz_reviewed,
            quiz_viewed, forums_viewed, page_views,
            resources_viewed, quiz_1, quiz_2, assignment, project]])
        
        return str(prediction[0])

        #return jsonify({'prediction': prediction[0][0]})
    except Exception as e:
        return jsonify({'error': str(e)})
