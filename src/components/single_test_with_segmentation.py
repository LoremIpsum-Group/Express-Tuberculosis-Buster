# NOT CONFIGURED PROPERLY, because importing of paths here
# not corrected due to imports in core functions now being related
# to the "widget router"

from core_functions.dependencies_loading import (
    tf,
    keras,
    np,
    cv2,
    plt,
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    last_conv_layer_name,
    load_model,
)

from core_functions.load_models import load_model_unet, load_model_efficientNet
from core_functions.preprocessing_only import get_img_array, temporary_process
from core_functions.segmentation_only import segment_image
from core_functions.classifier_only import predict
from core_functions.grad_CAM_new import make_gradcam_heatmap, superimpose_heatmap_V3

model_unet_loaded = load_model_unet("assets\ml-model\\unet_V0_1_3.h5")
model_efficientNet_loaded = load_model_efficientNet("assets\ml-model\efficientnetB3_V0_6_1.h5")

def single_image_test_segment(testing_image_path, model_segmentation, model_classifier):

    original_image, masked_image, mask_result = segment_image(
        model_segmentation, testing_image_path
    )

    fig, axes = plt.subplots(
        nrows=1, ncols=1, figsize=(5, 7), subplot_kw={"xticks": [], "yticks": []}
    )

    # masked_image = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2RGB)
    preprocessed_img = get_img_array(masked_image)

    # mask_result =  cv2.cvtColor(mask_result, cv2.COLOR_GRAY2RGB)
    # mask_result_preprocessed = get_img_array(mask_result)

    print(
        f"masked image shape preprocessed (with added rgb channel to be used for classifier temporarily!): {preprocessed_img.shape}"
    )

    # Remove last layer's softmax
    model_classifier.layers[-1].activation = None

    # Generate Grad-CAM heatmap (replace arguments with actual values)
    heatmap = make_gradcam_heatmap(
        preprocessed_img, model_classifier, last_conv_layer_name
    )

    original_preprocessed, masked_preprocessed = temporary_process(
        original_image, masked_image
    )

    print(f"Original image shape preprocessed: {original_preprocessed.shape}")
    print(
        f"Masked image shape preprocessed without the additional channel: {masked_preprocessed.shape}"
    )

    superimposed_img = superimpose_heatmap_V3(
        original_preprocessed, masked_preprocessed, heatmap
    )

    # Prediction results
    # activating again the classifier
    model_classifier.layers[-1].activation = tf.keras.activations.sigmoid

    # Use the masked image already in here
    predicted_class, predicted_score_rounded = predict(
        model_classifier, preprocessed_img
    )
    # Put into words the predicted class label

    axes.imshow(superimposed_img)
    axes.axis("off")
    # Set title with desired information
    axes.set_title(
        f"Image: {testing_image_path}\nPredicted: {predicted_class}\nScore: {predicted_score_rounded} %",
        color="black",
    )

    plt.show()

print("single testing function WITH SEGMENTATION initializing success")

'''
good segmentation: 
assets\\Normal-2551.png
assets\Tuberculosis-640.png
'''

single_image_test_segment(
    "assets\\Normal-2551.png", model_unet_loaded, model_efficientNet_loaded
)
