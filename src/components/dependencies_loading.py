import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

# for gradCAM
import keras
import cv2
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
import matplotlib as mpl
import matplotlib.pyplot as plt

IMAGE_HEIGHT = 300
IMAGE_WIDTH = 300
last_conv_layer_name = "block6f_expand_conv"
