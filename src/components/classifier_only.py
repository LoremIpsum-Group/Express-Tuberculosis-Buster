import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

# Preprocessing function, size changeable if another model used kunwari si b3
def get_img_array(img_path, size=(300, 300,3)):
    img = load_img(img_path, target_size=size)
    array = img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return array

# Load model from file
def load_model_from_file(filename):
    model = load_model(filename)
    return model

# Prediction function
def predict(model, image_path):
    # kailangan kasi naka array si img
    image_array = get_img_array(image_path)

    prediction = model.predict(image_array)

    # Print the predicted class label
    if prediction[0][0] > 0.5:
        predicted_class = "tuberculosis"
    else:
        predicted_class = "non-tb"

    predicted_score_rounded = round(prediction[0][0], 1)
    return predicted_class, predicted_score_rounded
