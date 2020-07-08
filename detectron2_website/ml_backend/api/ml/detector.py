from .polygon import polygonize
import cv2 as cv2
import os 
import numpy as np

import detectron2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode


class Detector:

	def __init__(self):
		cwd = os.path.dirname(os.path.abspath(__file__))
		cfg = get_cfg()   
		cfg.merge_from_file(os.path.join(cwd, "model/config.yaml"))   
		cfg.MODEL.WEIGHTS = os.path.join(cwd, 'model/model.pth')
		cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  
		cfg.DATASETS.TEST = ("bays_val", )

		self.predictor = DefaultPredictor(cfg)
		self.cwd = cwd 


	def get_rendered_outputs(self, im, savename=None):
		outputs = self.predictor(im)
		dataset_name = "bays_val"
		metadata = MetadataCatalog.get(dataset_name)
		v = Visualizer(im[:, :, ::-1], metadata=metadata, scale=0.8, instance_mode=ColorMode.SEGMENTATION)
		v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

		img = v.get_image()
		if savename is not None:
			cv2.imwrite(f"{savename}", img)
		
		img = cv2.imencode('.jpg', img)[1].tobytes()
		
		return img


	def get_raw_outputs(self, im):
		outputs = self.predictor(im)
		return outputs


	def get_polygonal_outputs(self, im):
		predictions = self.predictor(im)
		masks = predictions['instances'].pred_masks
		masks = np.array(masks)

		response = []
		for instance in range(0, masks.shape[0]):
			poly = polygonize(masks[instance, :, :])
			response.append({
				"type": "Feature",
				"properties": {"category": "Parking Bay"},
				"geometry": {
					"coordinates": [poly],
					"type": "Polygon"
				},
				"centroid": {
					"coordinates": poly[0]
				}
			})

		return response

		



		