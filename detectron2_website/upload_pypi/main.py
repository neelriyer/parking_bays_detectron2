import cv2
import detectron2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode


class detectron_spot():

	def __init__(self):
		self.file_path = file
		self.image_object = None

	def get_image(self):
		try:
			self.image_object = cv2.imread(self.file_path)
		except:
			raise "Can't read Image"

	def run_inference(self):

		cfg = get_cfg()    # obtain detectron2's default config
		cfg.merge_from_file("my_config.yaml")   # load values from a file
		cfg.MODEL.WEIGHTS = 'model_final.pth'
		cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold for this model
		cfg.DATASETS.TEST = ("bays_val", )

		predictor = DefaultPredictor(cfg)
		outputs = predictor(self.image_object)

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
		img = cv2.imencode('.jpg', v.get_image())[1].tobytes()
		# cv.imwrite(curr_dir+'/img.jpg',v.get_image())

		return img

	def driver(self):
		get_image()
		return run_inference()

if __name__ == "__main__":
	file = 'output.png'
	img = detectron_spot(file).driver()



