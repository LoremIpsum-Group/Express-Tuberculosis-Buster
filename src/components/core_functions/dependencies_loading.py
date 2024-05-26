import os
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

# for db/ recording of output
import sqlite3

# for gradCAM / image manipulation (resizing, etc)
import keras
import cv2
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
import matplotlib as mpl
import matplotlib.pyplot as plt
# valid options: top_conv, block3a_project_conv, block6f_expand_conv, block7a_expand_conv, block6a_project_conv
last_conv_layer_name = "block6a_project_conv"

IMAGE_HEIGHT = 300
IMAGE_WIDTH = 300

# for temporarily storing output images into memory
import io
import base64
from PIL import Image