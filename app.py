from flask import Flask

app = Flask(__name__)


@app.route('/')
def class_size():
    return "hello world"

@app.route('/get_class_size', methods=['GET', 'POST'])
def schedule():
    return "v2"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)