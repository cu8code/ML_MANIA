from flask import Flask,request,redirect,url_for,send_from_directory,render_template,current_app
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MODEL_NAME="Skin_SIH.h5"
MODEL_DIR="model"
upload_folder = os.path.join(os.getcwd(),'img')
model_path=os.path.join(os.getcwd(),MODEL_DIR,MODEL_NAME)
TYPE=['Eczema','Warts','Melanoma','Atopic','Basal','Melanocytic','Benign','Psoriasis','Seborrheic','Tinea']

app = Flask(
    __name__,
    static_folder=os.path.join(os.getcwd(),'static'),
)
app.config['UPLOAD_FOLDER'] = upload_folder

app.logger.info("loading the ML model")
model=tf.keras.models.load_model(model_path)
# print(
#     model.summary()
# )
app.logger.info("ML model loaded")

try:
    os.mkdir(upload_folder)
    app.logger.info('create img direcotry')
except:
    app.logger.info('img direcotry already exists')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            (diseases_name,top_class_index,top_class_label,top_class_score) = pred(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"Top predicted class: {diseases_name}"
            # return redirect(url_for('download_file', name=filename))
    return current_app.send_static_file('index.html')

def pred(img_path1):
    target_size = (75, 100)  # Set the target size to match DenseNet121's input size
    channels = 3  # Number of color channels

    img = tf.keras.preprocessing.image.load_img(img_path1, target_size=target_size)
    img_array1 = tf.keras.preprocessing.image.img_to_array(img)

# Ensure the image has the correct number of channels
    if img_array1.shape[-1] != channels:
        raise ValueError(f"Input image should have {channels} channels, but got {img_array1.shape[-1]} channels.")

# Expand the dimensions of the image and preprocess it
    img_array1 = np.expand_dims(img_array1, axis=0)
    img_array1 = tf.keras.applications.resnet.preprocess_input(img_array1)
    predictions = model.predict(img_array1)
    top_class_index = np.argmax(predictions)
    top_class_label = top_class_index  # Assuming class labels are integers
    top_class_score = predictions[0, top_class_index]
    diseases_name = TYPE[top_class_index]

    # print(f"Top predicted class: {top_class_label} with score: {top_class_score:.2f}")

    return (diseases_name,top_class_index,top_class_label,top_class_score)
