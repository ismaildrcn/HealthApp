import numpy as np
import cv2
import os
from keras.models import load_model

class PneumoniaDetect():
    def Preprocessing(self, img):
        imgSize = 100
        imgRead = cv2.imread(img, 0)
        imgResize = cv2.resize(imgRead, (imgSize, imgSize))
        img = np.array(imgResize) / 255
        img = img.reshape(-1, imgSize, imgSize, 1)
        return img

    def detect(self, img):
        model = load_model('weights/pneumonia.h5')
        result = model.predict(img)[0][0] * 100
        return result
