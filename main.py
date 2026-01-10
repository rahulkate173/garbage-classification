from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import requests
import os

MODEL_SERVER = os.environ.get("MODEL_SERVER", "http://localhost:8000")
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "no file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "no selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        try:
            with open(path, "rb") as f:
                files = {"file": (filename, f, "application/octet-stream")}
                resp = requests.post(f"{MODEL_SERVER}/predict", files=files, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return jsonify({"error": f"model server error: {e}"}), 500
        return jsonify(data)
    return jsonify({"error": "invalid file type"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
