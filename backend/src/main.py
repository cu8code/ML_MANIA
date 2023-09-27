from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from flask_cors import CORS

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
MODEL_NAME = "Skin_SIH1.h5"
MODEL_DIR = "model"
TYPE = [
    "Eczema",
    "Warts",
    "Melanoma",
    "Atopic",
    "Basal",
    "Melanocytic",
    "Benign",
    "Psoriasis",
    "Seborrheic",
    "Tinea",
]
upload_folder = os.path.join(os.getcwd(), "img")
model_path = os.path.join(os.getcwd(),'backend', MODEL_DIR, MODEL_NAME)

app = Flask(
    __name__,
)
CORS(app)
app.config["UPLOAD_FOLDER"] = upload_folder

# loading our custome model ---------------------
model = tf.keras.models.load_model(model_path)
# end loading our custome model -----------------


try:
    os.mkdir(upload_folder)
    app.logger.info("create img direcotry")
except:
    app.logger.info("img direcotry already exists")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.router("/api/chatapp",method=['POST'])
def chatapp_api():
    return


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return {1: "please provide a file"}
    file = request.files["file"]
    if file.filename == "":
        return {1: "plase provide a file with a file name"}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        (diseases_name, _, _, _) = pred(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        )
        return {
            "type": diseases_name,
        }
    return {1: "error"}


def pred(img_path1):
    target_size = (75, 100)  # Set the target size to match DenseNet121's input size
    channels = 3  # Number of color channels

    img = tf.keras.preprocessing.image.load_img(img_path1, target_size=target_size)
    img_array1 = tf.keras.preprocessing.image.img_to_array(img)

    # Ensure the image has the correct number of channels
    if img_array1.shape[-1] != channels:
        raise ValueError(
            f"Input image should have {channels} channels, but got {img_array1.shape[-1]} channels"
        )

    # Expand the dimensions of the image and preprocess it
    img_array1 = np.expand_dims(img_array1, axis=0)
    img_array1 = tf.keras.applications.resnet.preprocess_input(img_array1)
    predictions = model.predict(img_array1)
    top_class_index = np.argmax(predictions)
    top_class_label = top_class_index  # Assuming class labels are integers
    top_class_score = predictions[0, top_class_index]
    diseases_name = TYPE[top_class_index]

    # print(f"Top predicted class: {top_class_label} with score: {top_class_score:.2f}")

    return (diseases_name, top_class_index, top_class_label, top_class_score)
