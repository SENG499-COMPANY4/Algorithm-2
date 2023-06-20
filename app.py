from flask import Flask, request, jsonify
from class_size_predictor import returnClassSize

app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(415)
def unsupported_media_type(e):
    return jsonify(error=str(e)), 415

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/predict_class_sizes', methods=['GET', 'POST'])
def class_size():
    if request.method == 'GET':
        try:
            response = jsonify(returnClassSize())
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    elif request.method == 'POST':
        try:
            data = request.json
            # TODO: Process data, update class size predictions
            return jsonify({"message": "Data received and processed"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 415

