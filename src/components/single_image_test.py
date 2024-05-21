# NOT CONFIGURED PROPERLY, because importing of paths here
# not corrected due to imports in core functions now being related
# to the "widget router"

from core_functions.dependencies_loading import (
    tf,
    np,
    cv2,
    plt,
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    last_conv_layer_name,
    load_model,
)

from core_functions.preprocessing_only import get_img_array_OLD, get_img_array_original
from core_functions.classifier_only import predict
from core_functions.grad_CAM_new import make_gradcam_heatmap, superimpose_heatmap

# what image to use
def single_image_test(testing_image_path, model):
    # setting up displaying size and such
    fig, axes = plt.subplots(
        nrows=1, ncols=1, figsize=(5, 7), subplot_kw={"xticks": [], "yticks": []}
    )

    # Find the index of the row where 'FILE PATH' input is in dataframe
    # row_of_interest = dataframe.loc[dataframe["FILE PATH"] == image_path]
    # true_class = row_of_interest.iloc[0]["label"]
    # img_name = row_of_interest.iloc[0]["FILE NAME"]

    # Get the image array
    preprocessed_img = get_img_array_OLD(
        testing_image_path, (IMAGE_HEIGHT, IMAGE_WIDTH, 3)
    )

    original_img = get_img_array_original(testing_image_path)

    # Using grad cam
    # Remove last layer's softmax
    model.layers[-1].activation = None

    # Generate Grad-CAM heatmap (replace arguments with actual values)
    heatmap = make_gradcam_heatmap(preprocessed_img, model, last_conv_layer_name)

    # Display the superimposed image
    superimposed_img = superimpose_heatmap(original_img, heatmap)

    # Prediction results
    # activating again the classifier
    model.layers[-1].activation = tf.keras.activations.sigmoid

    # Get the preprocessed image
    # preprocessed_img = get_img_array(image_path)

    predicted_class, predicted_score_rounded = predict(model, preprocessed_img)

    # coloring the label
    # if true_class == predicted_class:
    #     color = "green"
    # else:
    #     color = "red"

    axes.imshow(superimposed_img)
    axes.axis("off")
    # Set title with desired information
    axes.set_title(
        # f"Image: {img_name}\nTrue Label: {true_class}\nPredicted: {predicted_class}\nScore: {predicted_score_rounded}",
        # color=color,

         f"Image: {testing_image_path}\nPredicted: {predicted_class}\nScore: {predicted_score_rounded}",
        color="black",
    )

    plt.show()


print("single testing function initializing success")

model = load_model('assets/ml-model/efficientnetB3_V0_6_1.h5')
single_image_test("assets\Tuberculosis-640.png", model)
