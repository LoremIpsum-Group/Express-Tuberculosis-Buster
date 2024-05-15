from components.dependencies_loading import tf, np, cv2, plt, IMAGE_HEIGHT, IMAGE_WIDTH, last_conv_layer_name, load_model

from grad_CAM_test import get_img_array, make_gradcam_heatmap, superimpose_heatmap

# what image to use
def single_image_test(testing_image_path, model):
    # setting up displaying size and such
    fig, axes = plt.subplots(
        nrows=1, ncols=1, figsize=(5, 7), subplot_kw={"xticks": [], "yticks": []}
    )

    # manually replace ang filepath here if gusto iba itest
    image_path = testing_image_path

    # Find the index of the row where 'FILE PATH' input is in dataframe
    # row_of_interest = dataframe.loc[dataframe["FILE PATH"] == image_path]
    # true_class = row_of_interest.iloc[0]["label"]
    # img_name = row_of_interest.iloc[0]["FILE NAME"]
    img_name = testing_image_path
    # Load the original image
    original_img = cv2.imread(image_path)

    # Get the image array
    preprocessed_img = get_img_array(image_path, (IMAGE_HEIGHT, IMAGE_WIDTH, 3))

    # Using grad cam
    # Remove last layer's softmax
    model.layers[-1].activation = None

    # Generate Grad-CAM heatmap (replace arguments with actual values)
    heatmap = make_gradcam_heatmap(preprocessed_img, model, last_conv_layer_name)

    # Display the superimposed image
    superimposed_img = superimpose_heatmap(image_path, heatmap)

    # Prediction results
    # activating again the classifier
    model.layers[-1].activation = tf.keras.activations.sigmoid

    # Get the preprocessed image
    # preprocessed_img = get_img_array(image_path)

    prediction = model.predict(preprocessed_img)
    # Put into words the predicted class label
    if (
        prediction[0][0] > 0.5
    ):  # adjustable, will be adjusted in the future according to Youden's index
        predicted_class = "tuberculosis"
    else:
        predicted_class = "non-tb"
    predicted_score_rounded = "{:.2f}".format(prediction[0][0])

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

         f"Image: {img_name}\nPredicted: {predicted_class}\nScore: {predicted_score_rounded}",
        color="black",
    )

    plt.show()


print("single testing function initializing success")

model = load_model('assets\ml-model\efficientNetB7_v0-5.h5')
single_image_test("assets\\x-ray.jpg", model)
