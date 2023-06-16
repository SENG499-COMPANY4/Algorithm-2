from flask import Flask
from class_size_predictor import returnClassSize

app = Flask(__name__)

@app.route('/predict_class_sizes', methods=['GET', 'POST'])
def class_size():
    if request.method == 'GET':
        return returnClassSize()
    elif request.method == 'POST':
        return "v2" # TODO: make function to save data

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)