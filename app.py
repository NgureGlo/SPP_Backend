from flask import Flask, request, jsonify
import pickle

# init Flask app
app = Flask(__name__)

# load model to app
with open('linear_regression_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# define endpoints for prediction
@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'message': 'welcome to flask app' })

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



if __name__ == '__main__':
    app.run(debug=True)