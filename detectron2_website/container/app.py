from ObjectDetector import Detector
import io
from flask import Flask, render_template, request, send_from_directory, send_file
from flask_cors import CORS
from PIL import Image
import flask
import requests
import os
import urllib.request
import uuid 
import cv2 
import img_transforms

app = Flask(__name__)
CORS(app)
detector = Detector()


#function to load img from url
def load_image_url(url):
	response = requests.get(url)
	img = Image.open(io.BytesIO(response.content))
	return img


@app.route("/")
def index():
	return render_template('index.html')


@app.route("/detect", methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':

		try:

			# open image
			file = Image.open(request.files['file'].stream)

			# remove alpha channel
			rgb_im = file.convert('RGB')

			# save as jpg
			rgb_im.save(os.getcwd()+'/file.jpg')

			print('image saved')
		
		# failure
		except:

			return render_template("failure.html")

	elif request.method == 'GET':

		# get url
		url = flask.request.args.get("url")

		# if jpg save 
		if('jpg' in str(url).lower()):

			# save image as jpg
			urllib.request.urlretrieve(url, os.getcwd()+'/file.jpg')

		# failure
		else:

			return render_template("failure.html")

		print('image saved')

	# get height, width of image
	original_img = Image.open(os.getcwd()+'/file.jpg')
	# height, width, channels = img.shape

	# # if image to big, return failure
	# if(height > 600 or width > 600):
	# 	return render_template("image_too_large.html")

	transformed_img = img_transforms._scale_to_square(original_img, targ=20*16)
	transformed_img.save(os.getcwd()+'/file_transformed.jpg')

	print('running detection...')
	# img = detector.run_detection	_image(os.getcwd()+'/file.jpg')
	untransformed_result = detector.detectron(os.getcwd()+'/file_transformed.jpg')
	untransformed_result = Image.open('/home/appuser/detectron2_repo/img.jpg')

	result_img = img_transforms._unsquare(untransformed_result, original_img)

	print('finished detection')

	# return render_template("return.html", text=text)

	try:
		os.remove(os.getcwd()+'/file.jpg')
		os.remove(os.getcwd()+'/file_transformed.jpg')
	except:
		pass

	# create file-object in memory
	file_object = io.BytesIO()

	# write PNG in file-object
	result_img.save(file_object, 'PNG')

	# move to beginning of file so `send_file()` it will read from start    
	file_object.seek(0)

	return send_file(file_object, mimetype='image/PNG')


	# return send_file(result_img,attachment_filename='image.jpg',mimetype='image/jpg')

	# return send_file(text, attachment_filename='filename.txt',mimetype='text/plain')
	# send_from_directory(directory = os.getcwd(), filename = text.split('/')[-1], as_attachment=True)

	# return send_from_directory(directory = os.getcwd(), filename = img.split('/')[-1], as_attachment=True) 


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port)
	# app.run(host='0.0.0.0')


