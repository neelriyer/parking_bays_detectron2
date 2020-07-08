from flask import Blueprint 
from flask import request, send_file, url_for, jsonify
from flask_cors import CORS

from api import auth

from detector import Detector
from utils import load_image_from_url, load_image_from_formdata 
from tasks import  async_predict_rendered

import io
import uuid
import os
import cv2

ml = Blueprint('ml', __name__, static_folder="static")
ml.detector = Detector()
ml.cwd = os.path.dirname(os.path.abspath(__file__))
CORS(ml)

@ml.route('/')
def index():
    return "ML index page"



@ml.route('/rendered', methods=["POST", "GET"])
@auth.login_required
def rendered():
	if request.method == 'POST':
		img = load_image_from_formdata(request.files['file'].stream)

	elif request.method == 'GET':
		url = request.args.get("url")
		img = load_image_from_url(url)	
	
	rendered_image_name = f"{uuid.uuid4()}.png"
	output_file_name = f"{ml.cwd}/static/{rendered_image_name}"
	rendered = ml.detector.get_rendered_outputs(img, savename=output_file_name)

	response = {
		"successful": True,
		"data":  {
			"url": url_for('ml.static', filename=rendered_image_name, _external=True)
		}
	}

	return jsonify(response)




@ml.route('/async/rendered', methods=["POST", "GET"])
@auth.login_required
def async_rendered():
	tmp_img = f"/tmp/{uuid.uuid4()}.png"
	if request.method == 'POST':
		img = load_image_from_formdata(request.files['file'].stream)
		
	elif request.method == 'GET':
		url = request.args.get("url")
		img = load_image_from_url(url)	

	cv2.imwrite(tmp_img, img)
	
	rendered_image_name = f"{uuid.uuid4()}.png"
	output_file_name = f"{ml.cwd}/static/{rendered_image_name}"
	job = async_predict_rendered.apply_async(args=[tmp_img, output_file_name])

	response = {
		"successful": True,
		"data":  {
			"jobid": job.id
		}
	}

	return jsonify(response), 200



@ml.route('/polygons', methods=["GET"])
@auth.login_required
def polygons():
	url = request.args.get("url")
	img = load_image_from_url(url)	
	
	predictions = ml.detector.get_polygonal_outputs(img)
	
	response = {
		"successful": True,
		"data": predictions
	}
	return jsonify(response)
