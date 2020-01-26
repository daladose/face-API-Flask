from flask import Flask, json, Response, request, render_template
from werkzeug.utils import secure_filename
import base64
from os import path, getcwd
import os
import time
from finding_face import *
from recognizer import Recognizer


app = Flask(__name__)


app.config['file_allowed'] = ['image/png', 'image/jpeg']
app.config['storage'] = path.join(getcwd(), 'storage')
app.config['after_crop_image'] = path.join(getcwd(), 'storage/croped_images')
app.config['app_path'] = path.dirname(os.path.abspath(__file__))
app_path = path.dirname(os.path.abspath(__file__))
app.recognizer = Recognizer(app)


def create_directory_before_crop_images(username):
    user_directory = path.join(app.config['storage'], 'pre_croped_images')
    try:
        os.mkdir(user_directory+"/"+username)
    except FileExistsError:
        print("You already have directory name ",username)


def create_directory_after_crop_images(username):
    output_directory = path.join(app.config['storage'], 'croped_images')
    try:
        os.mkdir(output_directory+"/"+username)

    except FileExistsError:
        print("You already have directory name ",username)


def upload_to_before_crop_images(username):
    target = os.path.join ( app_path, "storage/pre_croped_images/"+username)
    print ( target )

    if not os.path.isdir ( target ):
        os.mkdir ( target )

    for file in request.files.getlist ( "file" ):
        print ( file )
        filename = file.filename
        destination = "/".join ( [target, filename] )
        print ( destination )
        file.save ( destination )

    return "Upload Success"


def train_model():
    registration_status = app.recognizer.recognize_face("./storage/croped_images", "./storage/unknown")
    registration_status_message = {"registration_status": registration_status}
    return success_handle(json.dumps(registration_status_message))


def decode_base64(imgstring, image_file_name):
    imgdata = base64.b64decode(imgstring)
    filename = image_file_name+".jpg"
    with open(app.config['storage']+"/unknown/"+filename, 'wb') as f:
        f.write(imgdata)
    return filename


def encode_base64(path):
    with open(path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read())
    return base64_string


def success_handle(output, status=200, mimetype='application/json'):
    return Response(output, status=status, mimetype=mimetype)


def error_handle(error_message, status=500, mimetype='application/json'):
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)


# api version
@app.route('/api', methods=['GET'])
def api_version():
    output = json.dumps({"api": '1.0'})
    return success_handle(output)


# Register process
@app.route('/api/regist_face', methods=['POST'])
def registration():
    message = "success"

    username = request.form['username']


    # create directory for this username inorder to save image Before croped
    create_directory_before_crop_images(username)

    # create directory for this username inorder to save image After croped
    create_directory_after_crop_images(username)

    before_crop_image_dir = path.join ( app_path, "storage/pre_croped_images/"+username)
    upload_to_before_crop_images(username)

    # process croping face an image
    crop_face_process(username,before_crop_image_dir)

    # train
    message = train_model()

    # return success_handle(json.dumps(message))
    return message


@app.route('/api/predict/<string:ref>', methods=['POST'])
def predict_person(ref):
    send_time = int(time.time())
    image_id = "{}{}".format(ref, send_time)
    str = encode_base64("obama.jpg")
    test_pic_dir = decode_base64(str, image_id)

    predict_message = app.recognizer.predictor_face(test_pic_dir)
    # predict_message = {"predict_person": predict_person}
    return success_handle(json.dumps(predict_message))


# encodeB64
@app.route('/encodeB64', methods=['GET'])
def encodeB64():
    str = encode_base64("obama.jpg")
    print(encode_base64("obama.jpg"))
    return str

# A welcome message to test our server
@app.route('/')
def homepage():
    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template('homepage.html')


# Run the app
if __name__ == '__main__':
    app.run()
