import cv2
from cv2 import dnn

sr = dnn.DnnSuperResImpl_create()
path = 'EDSR_x4.pb'
sr.readModel(path)
