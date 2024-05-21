from components.core_functions.dependencies_loading import(
    tf,
    load_model,
    load_img, img_to_array,
    np
)

from components.core_functions.preprocessing_only import get_img_array

# Load model from file
def load_model_from_file(filename):
    model = load_model(filename)
    return model

# Prediction function
def predict(model, image):
    # kailangan kasi naka array si img
    image_array = get_img_array(image)

    prediction = model.predict(image_array)

    # Print the predicted class label
    if prediction[0][0] > 0.5:
        predicted_class = "Tuberculosis"
    else:
        predicted_class = "Non-TB"

    predicted_score_rounded = round( (prediction[0][0] * 100.0), 2 )

    return predicted_class, predicted_score_rounded
