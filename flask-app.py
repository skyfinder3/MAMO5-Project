from flask import Flask, request, jsonify

from subprocess_caller import analyze_image

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.json

    result = {
        "output": analyze_image(data["text"])
    }
    return jsonify(result)

@app.route("/", methods=['GET'])
def home():
    return "Up and Running"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)


