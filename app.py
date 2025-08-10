from flask import Flask, jsonify


app = Flask(__name__)

@app.route("/status", methods=["GET"])
def deployment_status():
    return jsonify(message="deployment is SUCCESSFUL"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
