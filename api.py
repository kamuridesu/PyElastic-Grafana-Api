from flask import Flask, jsonify, request
try:
    from main import GitlabAnalElastic
except:
    from .main import GitlabAnalElastic


app = Flask(__name__)
ganal = GitlabAnalElastic("http://elastic:9200")


@app.route("/")
def index():
    return jsonify({"message": "Hello World!"})


@app.route("/content/<id>", methods=['GET'])
def get_content(id):
    return jsonify(ganal.get_content("test-index", id))


@app.route("/content/<index>", methods=['PUT'])
def put_content(index):
    content = request.get_json()
    return jsonify(ganal.add_content(index, content))


@app.route("/content/<index>", methods=['POST'])
def post_content(index):
    content = request.get_json()
    return jsonify(ganal.put_content(index, content['id'], content))


@app.route("/content/<index>/<id>", methods=['DELETE'])
def delete_content(index, id):
    return jsonify(ganal.delete_content(index, id))


@app.route("/content/<index>/<id>", methods=['GET'])
def get_content_by_id(index, id):
    return jsonify(ganal.get_content(index, id))


@app.route("/content/<index>", methods=['GET'])
def get_content_by_index(index):
    return jsonify(ganal.get_content_by_index(index))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
