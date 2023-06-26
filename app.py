from flask import Flask, request, jsonify
from class_size_predictor import returnClassSize

app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error=str(e)), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/predict_class_sizes', methods=['GET', 'POST'])
def class_size():
    if request.method == 'POST':
        try:
            response = jsonify(returnClassSize(request.json)), 200
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "405: Method not allowed"}), 405