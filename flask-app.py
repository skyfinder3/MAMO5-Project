from flask import Flask, request, jsonify

from my_script import do_something

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.json

    result = {
        "output": do_something(data["text"])
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)


