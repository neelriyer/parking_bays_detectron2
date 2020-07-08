from ObjectDetector import Detector
import io
from flask import Flask, render_template, request, send_from_directory, send_file
from PIL import Image
from flask import send_file
import flask
import requests
import os
import urllib.request
import uuid 
import cv2 

app = Flask(__name__)
detector = Detector()


#function to load img from url
def load_image_url(url):
	response = requests.get(url)
	img = Image.open(io.BytesIO(response.content))
	return img


@app.route("/")
def index():
	return render_template('index.html')



@app.route("/classify", methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		file = Image.open(request.files['file'].stream)
		img = detector.detectObject(file)
		return send_file(io.BytesIO(img),attachment_filename='image.jpg',mimetype='image/jpg')
	elif request.method == 'GET':
		url = flask.request.args.get("url")
		print(url)
		file = load_image_url(url)
		img = detector.detectObject(file)
		return send_file(io.BytesIO(img),attachment_filename='image.jpg',mimetype='image/jpg')


@app.route("/mask_rcnn", methods=['POST', 'GET'])
def mask_rcnn():

	if request.method == 'POST':
		file = request.files['file']
		file.save(os.getcwd()+'/file.jpg')
		filepath = os.getcwd()+'/file.jpg'

	elif (request.method == 'GET'):

		# get url
		url = flask.request.args.get("url")
		print(url)

		# save image in cwd
		filepath = os.getcwd()+'/file.jpg'
		urllib.request.urlretrieve(url, filepath)


	# run detection
	file = detector.mask_RCNN(filepath)

	return send_file(file, attachment_filename='filename.txt',mimetype='text/plain')


	# return send_file(io.BytesIO(file),attachment_filename='image1.jpg',mimetype='image1/jpg')


@app.route("/parkinglot_detection", methods=['GET'])
def upload_parking():

	if request.method == 'GET':
		# get url
		url = flask.request.args.get("url")
		print(url)

		# save image in cwd
		filepath = os.getcwd()+'/file.jpg'
		urllib.request.urlretrieve(url, filepath)

		img = detector.run_detection_image(filepath)

		return send_file(io.BytesIO(img),attachment_filename='image1.jpg',mimetype='image1/jpg')



if __name__ == "__main__":
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port)
	# app.run(host='0.0.0.0')


