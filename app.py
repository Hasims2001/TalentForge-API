from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def Documentation():
    return jsonify({'issue': False, 'message': "Welcome to TalentForge"})


# if __name__ == "__main__":
#     app.run()