import numpy as np
import cv2
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


class brainTumorDetect():
    def Preprocessing(self, img):
        imgSize = 100
        imgRead = cv2.imread(img)
        img = cv2.resize(imgRead, (imgSize, imgSize))
        img = np.array(img)
        img = img.reshape(-1, imgSize, imgSize, 3)
        return img

    def detect(self, img):
        labels = ['glioma','meningioma','no tumor','pituitary']
        model = load_model('weights/brainTumor.h5')
        results = model.predict(img)
        results = [x * 100 for x in results[0]]

        counter = 0
        value = 0
        for result in results:
            if result > value:
                value = result
                label = labels[counter]
            counter += 1
        return value, label
