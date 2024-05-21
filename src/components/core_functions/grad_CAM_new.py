from components.core_functions.dependencies_loading import (
    tf,
    keras,
    np,
    cv2,
    plt,
    mpl,
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    last_conv_layer_name,
    load_model,
)

from components.core_functions.preprocessing_only import temporary_process, get_img_array, get_img_array_OLD

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]
    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

# For test case where no segmented image present
def superimpose_heatmap(original_img, heatmap, alpha=0.3):
    # Assuming heatmap is your original array
    heatmap[np.isnan(heatmap)] = (
        0  # Replace NaN values with 0, ensures na fluid flow ng program even if pixel errors
    )

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = mpl.colormaps["jet"]

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap. temporarily convert to img
    jet_heatmap = keras.utils.array_to_img(jet_heatmap)
    #jet_heatmap = jet_heatmap.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    
    # Get the size of the original image
    original_img_size = original_img.shape[:2]
    # Resize the heatmap, then return it to array
    jet_heatmap = jet_heatmap.resize(original_img_size)
    jet_heatmap = keras.utils.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + original_img
    superimposed_img = keras.utils.array_to_img(superimposed_img)

    # Save the superimposed image
    # superimposed_img.save(cam_path)

    # Display Grad CAM
    # display(Image(cam_path))

    return superimposed_img

# ONLY RETUNS SEGMENTED IMAGE WITH GRADCAM, not superimposed into original img
def superimpose_heatmap_V3(original_img, segmented_img, heatmap, alpha=0.3):
    """
    Superimposes the heatmap onto the original image, restricted to the regions defined by the segmented image.

    Args:
        original_img (numpy.ndarray): The original image.
        segmented_img (numpy.ndarray): The segmented image defining the regions of interest.
        heatmap (numpy.ndarray): The heatmap to be superimposed.
        alpha (float, optional): The blending factor for the heatmap. Defaults to 0.4.

    Returns:
        numpy.ndarray: The superimposed image.
    """
    # Convert heatmap to RGB format using the jet colormap
    heatmap_jet = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)

    # Resize the heatmap to match the dimensions of the original image
    heatmap_resized = cv2.resize(
        heatmap_jet, (original_img.shape[1], original_img.shape[0])
    )

    # Convert segmented image to binary mask
    binary_mask = (segmented_img > 0).astype(np.uint8)

    # Expand dimensions of binary mask to match the number of channels in the heatmap
    # binary_mask_expanded = np.expand_dims(binary_mask, axis=-1)

    # Apply the binary mask to the heatmap
    # heatmap_masked = heatmap_resized * binary_mask_expanded

    heatmap_masked = heatmap_resized * binary_mask

    # Convert original image to uint8 for compatibility with addWeighted
    original_img_uint8 = cv2.convertScaleAbs(original_img)

    # Blend the masked heatmap with the original image
    superimposed_img = cv2.addWeighted(
        original_img_uint8, 1 - alpha, heatmap_masked, alpha, 0
    )

    return superimposed_img

# SUPERIMPOSING THE GENERATED GRAD CAM FROM SEGMENTED IMAGE, ONTO ORIGINAL IMAGE
def get_gradCAM(model_classifier, original_image, masked_image):
    # Remove last layer's softmax
    model_classifier.layers[-1].activation = None

    preprocessed_img = get_img_array(masked_image)

    # Generate Grad-CAM heatmap (replace arguments with actual values)
    heatmap = make_gradcam_heatmap(
        preprocessed_img, model_classifier, last_conv_layer_name
    )

    original_preprocessed, masked_preprocessed = temporary_process(
        original_image, masked_image
    )

    superimposed_img = superimpose_heatmap_V3(
        original_preprocessed, masked_preprocessed, heatmap
    )
    # activating again the classifier
    model_classifier.layers[-1].activation = tf.keras.activations.sigmoid

    return superimposed_img


def get_gradCAM_NONSEGMENTED(model_classifier, original_image):
    # Remove last layer's softmax
    model_classifier.layers[-1].activation = None

    preprocessed_img = get_img_array_OLD(original_image)

    # Generate Grad-CAM heatmap (replace arguments with actual values)
    heatmap = make_gradcam_heatmap(
        preprocessed_img, model_classifier, last_conv_layer_name
    )

    superimposed_img = superimpose_heatmap(preprocessed_img, heatmap)
    
    # activating again the classifier
    model_classifier.layers[-1].activation = tf.keras.activations.sigmoid

    return superimposed_img
