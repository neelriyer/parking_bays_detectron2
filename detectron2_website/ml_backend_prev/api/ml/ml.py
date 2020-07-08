from flask import Blueprint 
from flask import request, send_file, url_for, jsonify
from flask_cors import CORS
from .detector import Detector
from .utils import load_image_from_url, load_image_from_formdata 
import io
import uuid
import os

ml = Blueprint('ml', __name__, static_folder="static")
ml.detector = Detector()
ml.cwd = os.path.dirname(os.path.abspath(__file__))
CORS(ml)

@ml.route('/')
def index():
    return "ML index page"

@ml.route('/rendered', methods=["POST", "GET"])
def rendered():
	if request.method == 'POST':
		img = load_image_from_formdata(request.files['file'].stream)

	elif request.method == 'GET':
		url = request.args.get("url")
		print(url)
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

@ml.route('/polygons', methods=["GET"])
def polygons():
	url = request.args.get("url")
	img = load_image_from_url(url)	
	
	predictions = ml.detector.get_polygonal_outputs(img)
	
	response = {
		"successful": True,
		"data": predictions
	}
	return jsonify(response)
