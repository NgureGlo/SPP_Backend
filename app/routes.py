from flask import flash, request, jsonify
from app import app, db, loaded_model
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import Bcrypt
from app.models import User
from app.models import Course


@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'message': 'welcome to flask app' })

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

        user = User(name=name, email=email, password=password)
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
           
            return jsonify({'meessage': 'Login successful!', 'uid' : user.id})
    else:
            # Login failed, show error message
            return jsonify({'message': 'Invalid email or password.'})
    

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

    course_id = str(data['course_id'])
    course_level = str(data['course_level'])
    course_name = str(data['course_name'])
    current_user_id = int(data['current_user_id'])
    
    if course_id and course_level and course_name:
        added_by = current_user_id  # Assuming current_user is the logged-in user
        course = Course(course_id=course_id, course_level=course_level, course_name=course_name, added_by=added_by)
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
