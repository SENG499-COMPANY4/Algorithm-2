from flask import Flask, request, jsonify
from class_size_predictor import returnClassSize

app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/predict_class_sizes', methods=['GET', 'POST'])
def class_size():
    if request.method == 'GET':
        response = jsonify(returnClassSize())
        return response
    elif request.method == 'POST':
        data = request.json
        # TODO: Process data, update class size predictions
        return jsonify({"message": "Data received and processed"}), 200

