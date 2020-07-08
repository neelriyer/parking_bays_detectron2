from celery import Task
from .detector import Detector
from .utils import load_image_from_url, load_image_from_formdata 
from api import celery
import cv2
import os
import uuid

cwd = os.path.dirname(os.path.abspath(__file__))

class PredictionWorker(Task):
    def __init__(self):
        self.detector = Detector()

@celery.task(base=PredictionWorker)
def async_predict_rendered(img, savename):
    img = cv2.imread(img)
    rendered = async_predict_rendered.detector.get_rendered_outputs(img, savename=savename)


