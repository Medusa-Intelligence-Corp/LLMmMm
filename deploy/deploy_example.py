import csv
import os
import json
import requests
import time

import tensorflow as tf  # USE TENSORFLOW 2.2
import numpy as np
import pandas as pd


img_height = 227
img_width = 227
image_path = 'deploy/alpha-score'
MODEL_PATH = 'train/model_output/alpha-score'


def setup_model():
    filename = os.path.join(os.getcwd(), MODEL_PATH,
                                      "/model_v001")
    model = tf.keras.models.load_model(filename)
    return model


def image_preprocessing(image_path, img_height, img_width):
    full_path = os.path.join(os.getcwd(), image_path)
    image = tf.keras.preprocessing.image.load_img(full_path, color_mode='rgb', target_size=(img_height, img_width))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    return input_arr


def predict(model, input_arr):
    pred_followers = model.predict(np.array([input_arr]))
    return pred_followers[0][0] * 100


def main():
    model = setup_model()
    input_arr = image_preprocessing(image_path + 'test_image.jpg', img_height, img_width)
    prediction = predict(model, input_arr)
    print('Prediction: ' + str(int(prediction)) + '% that image is popular')



if __name__ == "__main__":
    main()
