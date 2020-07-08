import cv2 as cv
import os
import subprocess
import urllib.request
import json
import numpy as np
import random
import os
import numpy
# import keras
# from keras_retinanet import models
# from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
# from keras_retinanet.utils.visualization import draw_box, draw_caption
# from keras_retinanet.utils.colors import label_color
# import tensorflow as tf
# import argparse
from PIL import Image
from PIL import ImageDraw
import io
import time


# existing detector dunctions
class Detector:

	# # retinanet model
	# def run_detection_image(self, filepath):

	# 	# read image
	# 	image = read_image_bgr(filepath)

	# 	# load model
	# 	model_path = 'model/parkinglots_driveway/resnet50_csv_12_inference.h5'
	# 	model = models.load_model(model_path, backbone_name='resnet50')
	# 	labels_to_names = {0: 'parkinglot', 1: 'driveway'}

	#	# copy to draw on
	# 	draw = image.copy()
	# 	draw = cv.cvtColor(draw, cv.COLOR_BGR2RGB)

	# 	# preprocess image for network
	# 	image = preprocess_image(image)
	# 	image, scale = resize_image(image)

	# 	# process image
	# 	start = time.time()
	# 	boxes, scores, labels = model.predict_on_batch(numpy.expand_dims(image, axis=0))
	# 	print("processing time: ", time.time() - start)

	# 	# correct for image scale
	# 	boxes /= scale

	# 	# visualize detections
	# 	for box, score, label in zip(boxes[0], scores[0], labels[0]):
	# 		# scores are sorted so we can break
	# 		if score < 0.5:
	# 			break

	# 		color = label_color(label)
			
	# 		b = box.astype(int)
	# 		draw_box(draw, b, color=color)

	# 		try:
	# 			caption = "{} {:.3f}".format(labels_to_names[label], score)
	# 			draw_caption(draw, b, caption)
	# 		except:
	# 			pass


	# 	file, ext = os.path.splitext(filepath)
	# 	image_name = file.split('/')[-1] + ext
	# 	output_path = os.path.join('examples/results/', image_name)
		
	# 	draw_conv = cv.cvtColor(draw, cv.COLOR_BGR2RGB)
	# 	img = draw_conv
	# 	img = cv.imencode('.jpg', img)[1].tobytes()
	# 	#cv.imwrite(output_path, draw_conv)

	# 	return img

	# vanilla model	
	def detectObject(self, imName):

		cvNet = cv.dnn.readNetFromTensorflow('model/object_detection/frozen_inference_graph.pb','model/object_detection/ssd_mobilenet_v1_coco_2017_11_17.pbtxt')
		img = cv.cvtColor(numpy.array(imName), cv.COLOR_BGR2RGB)
		cvNet.setInput(cv.dnn.blobFromImage(img, 0.007843, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
		detections = cvNet.forward()
		cols = img.shape[1]
		rows = img.shape[0]

		for i in range(detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > 0.5:
				class_id = int(detections[0, 0, i, 1])

				xLeftBottom = int(detections[0, 0, i, 3] * cols)
				yLeftBottom = int(detections[0, 0, i, 4] * rows)
				xRightTop = int(detections[0, 0, i, 5] * cols)
				yRightTop = int(detections[0, 0, i, 6] * rows)

				cv.rectangle(img, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
										 (0, 0, 255))
				if class_id in classNames:
					label = classNames[class_id] + ": " + str(confidence)
					labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
					yLeftBottom = max(yLeftBottom, labelSize[1])
					cv.putText(img, label, (xLeftBottom+5, yLeftBottom), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

		img = cv.imencode('.jpg', img)[1].tobytes()
		return img


	# detectron model	
	def detectron(self, file):

		import detectron2
		from detectron2.engine import DefaultPredictor
		from detectron2.config import get_cfg
		from detectron2.data import MetadataCatalog
		from detectron2.utils.visualizer import Visualizer
		from detectron2.utils.visualizer import ColorMode

		curr_dir = '/home/appuser/detectron2_repo'
		print(os.getcwd())

		cfg = get_cfg()    # obtain detectron2's default config
		cfg.merge_from_file("my_config.yaml")   # load values from a file
		file_name = curr_dir+'/model_final.pth'


		cfg.MODEL.WEIGHTS = file_name
		cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold for this model
		cfg.DATASETS.TEST = ("bays_val", )

		predictor = DefaultPredictor(cfg)

		im = cv.imread(file)
		outputs = predictor(im)

		# with open(curr_dir+'/data.txt', 'w') as fp:
		# 	json.dump(outputs['instances'], fp)
		# 	# json.dump(cfg.dump(), fp)

		# register data
		dataset_name = "bays_val"
		# DatasetCatalog.register(dataset_name, get_training_dicts_real_val)
		# MetadataCatalog.get(dataset_name).set(thing_classes=["Bay", "Disabled"])
		metadata = MetadataCatalog.get(dataset_name)

		# visualise this piece of shit
		v = Visualizer(im[:, :, ::-1], metadata=metadata, scale=0.8, instance_mode=ColorMode.SEGMENTATION)
		v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
		# cv2_imshow(v.get_image()[:, :, ::-1])

		# write to jpg
		img = cv.imencode('.jpg', v.get_image())[1].tobytes()
		cv.imwrite(curr_dir+'/img.jpg',v.get_image())

		return img

		# render_html
		# return str(outputs["instances"]), curr_dir+'/img.jpg'



		