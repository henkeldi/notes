#/usr/bin/python
# -*- coding: utf-8 -*-
'''
1. Loads a model from tf hub
2. Opens Webcam stream
3. Continously performs classification
'''

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2

def main():
    classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"

    model = tf.keras.Sequential([
        hub.KerasLayer(classifier_url , output_shape=[1001])
    ])
    model.build([None, 224, 224, 3])  # Batch input shape.

    labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
    imagenet_labels = np.array(open(labels_path).read().splitlines())

    cap = cv2.VideoCapture(0)

    key = -1
    # While escape key not pressed classify image
    while key != 27:
        ret, frame = cap.read()
        if ret:
            resized_image = cv2.resize(frame, (224, 224)) / 255.0
            result = model.predict(resized_image[np.newaxis, ...])
            predicted_class = np.argmax(result)
            predicted_class_name = imagenet_labels[predicted_class]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, predicted_class_name, (10, 60), font, 1, (255,255,255), 2, cv2.LINE_AA)
            cv2.imshow('Prediction', frame)

        key = cv2.waitKey(1)

if __name__ == '__main__':
    main()

