import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image


import tensorflow as tf
import keras.backend as K
import keras
from keras.models import load_model

from keras.models import *
from keras.layers import *
from keras.optimizers import *

# from core_functions import load_model_efficientNet, load_model_unet


IMAGE_HEIGHT, IMAGE_WIDTH = 512, 512
last_conv_layer_name = "top_conv"


# ------ START LOADING MODEL------#
def load_model_efficientNet(path):
    model = load_model(path)
    return model


def load_model_unet(path):
    # Segment for loading the unet model
    @keras.utils.register_keras_serializable()
    def dice_coef(y_true, y_pred):
        y_true_f = y_true.flatten()
        y_pred_f = y_pred.flatten()
        intersection = keras.sum(y_true_f * y_pred_f)
        return (2.0 * intersection + 1) / (
            keras.sum(y_true_f) + keras.sum(y_pred_f) + 1
        )

    @keras.utils.register_keras_serializable()
    def dice_coef_loss(y_true, y_pred):
        return -dice_coef(y_true, y_pred)

    tf.keras.utils.get_custom_objects()["dice_coef_loss"] = dice_coef_loss
    model = load_model(
        path,
        custom_objects={"dice_coef_loss": dice_coef_loss},
    )

    return model

# ------ END LOADING MODEL------#


# -----START PREPROCESSING STUFFS-----#
def check_image(image_path):
    print("\n\n---Start of Checking input image---\n")
    """
    Input validation for image file. Not-so comprehensive checks for now are in here. Expandable
    Parameters:
    image_path (str): The path to the image file.

    Returns:
    FAULTY_IMG (bool): True if the image is not suitable for the model, False otherwise.

    This function reads an image from the specified path and checks if the image is
    mostly black or white, which might indicate an issue with the image. It also checks
    if the mean pixel value of the normalized image is close to the expected value.
    (That value is calculated based on the mean value of pixels in training dataset, used in the segmentation model.)

    """
    FAULTY_IMG = False
    message= "The image color appears to be within acceptable ranges."
    # Load the image
    image = cv2.imread(image_path)

    #! Code below checks if Image is black (pixel values close to 0) or white,
    #! indicates issue with image itself. Can be used as error catching
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean_pixel_value = np.mean(gray_image)
    # Get normalized img (normalized using same method in segmentation for uniformity)
    normalized_img = (gray_image - 127.0) / 127.0
    mean_normalized_value = np.mean(normalized_img)
    # Define threshold values for different colors
    threshold_black = 50
    threshold_white = 220

    print(image.shape[0], image.shape[1])
    if image.shape[0] < 512 or image.shape[1] < 512:
        message = "The image size is smaller than the minimum required size of 512x512 pixels."
        FAULTY_IMG = True
        return FAULTY_IMG, message

    if mean_pixel_value < threshold_black:
        message = "The image appears to be mostly black"
        FAULTY_IMG = True
    elif mean_pixel_value > threshold_white:
        message = "The image appears to be mostly white"
        FAULTY_IMG = True
    elif not np.isclose(mean_normalized_value, 0.17, atol=0.15):
        message = "Image migth be darker or brighter than expected.\nSegmentation might be affected."
    else:
        pass
    print("\n\n---End of Checking input image---\n")
    return FAULTY_IMG, message


# Special preprocessing function for cropping image
def crop_resize_image(path):

    print("\n\n---Start of preprocessing input (cropping and resizing for now---\n")
    """
    #! All other kinds of preprocessing like if want i pa brighten, will be done here, meaning function name will be changed
    The function works by finding all non-zero pixels in the image using the cv2.findNonZero function.
    These non-zero pixels represent the region of interest in the mask. (Basically crop out plain background)
    

    Parameters:
    image (Path file)
    Returns:
    cropped_image (numpy array): The cropped and resized image, or None if the image is empty.

    If there are no non-zero pixels (i.e., the mask is empty), the function returns None.
    If there are non-zero pixels, the function calculates the minimum bounding rectangle that encloses
    all non-zero pixels using the cv2.boundingRect function.
    This rectangle represents the smallest possible region that contains all the non-zero pixels.
    The function then crops the image to this bounding rectangle and returns the cropped image.

    """
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Determine the binarization method based on the mean pixel value
    if np.mean(image) > 127:
        binarization_method = cv2.THRESH_BINARY_INV
    else:
        binarization_method = cv2.THRESH_BINARY

    # Binarize the image using Otsu's thresholding
    _, binarized_image = cv2.threshold(
        image, 0, 255, binarization_method + cv2.THRESH_OTSU
    )

    non_zero_pixels = cv2.findNonZero(binarized_image)

    if non_zero_pixels is None:
        print(
            " If tumakbo to, then somehow naka input ng image na di naman existing. WTF"
        )

        return None

    x, y, w, h = cv2.boundingRect(non_zero_pixels)

    cropped_image = image[y : y + h, x : x + w]

    # *Resizing happens here
    cropped_image = cv2.resize(
        cropped_image, (IMAGE_HEIGHT, IMAGE_WIDTH), interpolation=cv2.INTER_CUBIC
    )

    print("\n\n---End of preprocessing input (cropping and resizing for now---\n")
    return cropped_image


def check_segmented_img(segmented_img, mask_created):

    print("\n\n---Start of simple checking of the segmented image---\n")
    message = "Segmented image not containing many artifacts"
    """
    Function dedicated for checking the image after being segmented. MUST BE COMPREHENSIVE AND SO MUST BE REVISED

    Returns:
    Faulty (bool): True if the image has been compromised during segmentation, False otherwise.
    """

    # * More advanced way of validating image, if image (most likely unrelated) is segmented into multiple parts
    # * because it is unreleated to the model or if the image quality is too bad, it will mot probably look like pebbles
    # * basta mukang spider web. If that happens, this will count the number of components in the image and if it is too high
    # * flag or warning can be done
    # Label the connected components in the segmented image
    num_components, labels = cv2.connectedComponents(segmented_img)

    # If the number of components is very high, raise a warning
    # Subtract 1 because the background is also considered a component
    # Count the number of unique labels (excluding the background label 0)
    num_components = len(np.unique(labels)) - 1

    if num_components > 2:
        message = "Warning: The segmented image might \nhave 'pebble-like' artifacts,image \nmost likely faulty"
        return True, message, num_components
    elif num_components >4:       
        message = "Warning: The segmented image has \nmany 'pebble-like' artifacts,image \nmost likely faulty"
        return True, message, num_components

    #! Code below checks if produced masked image is blank, indicates issue with applying mask itself. Can be used as error catching
    #! Technically repetetive, if mask is blank, then masked image is blank duh
    # IMAGE_BLANK_MASKEDIMG = np.allclose(mask_result, 0) # true if all values in mask_result are close to 0
    # print("MASKED IMAGE IS BLANK:", np.allclose(mask_result, 0))

    #! Code below checks if produced mask is blank, indicates issue with image itself. Can be used as error catching
    # IMAGE_BLANK_MASK = np.allclose(mask_result, 0) # true if all values in mask_result are close to 0
    # print("MASK IS BLANK:", np.allclose(mask_result, 0))

    if np.allclose(mask_created, 0) or np.allclose(segmented_img, 0):
        print("Mask is blank. Image is faulty!.")
        message = "Mask is blank. Image is faulty!."
        return True, message, num_components

    print("\n\n---End of simple checking of the segmented image---\n")
    return False, message, num_components


# ---- END OF PREPROCESSING STUFF----#


# -----START SEGMENTATION PROCESS-----#
def segment_imageV2(model, image, img_shape=(512, 512), threshold=127.0):
    print("\n\n---Start of Segmentation---\n")
    """
        Preprocesses image and then produce binary mask of object, which is then applied to original image to get only region of intetrest.

        Parameters:
            model (object): Segmentation model used for prediction.
            path (str): File path of the original image.
            img_shape (Tuple): Desired shape for resizing images.
            threshold (float): Threshold value for normalizing image (Used to adjust sensitivity of mask prediction, default is 127.0)

        Returns:
            tuple: A tuple containing the concerning images 
                Orig image data: (512, 512) | uint8 | 
                Masked image data: (512, 512) | uint8 |
                mask_result image data: (512, 512, 1) | bool |

        Description: 
        This function takes a filepath containing  original image.
        It processes the imageby resizing them to the desired shape, converting into grayscale, then normalizing pixel values to [-1,1].

        1. Grayscale: The image is converted to grayscale using the cv2.cvtColor function 
        with the cv2.COLOR_BGR2GRAY flag.

        2. Cropping: Crop out plain background using crop_image function. 
        This function works by finding all non-zero pixels in the image using the cv2.findNonZero function.

        3. Resizing: INTER_CUBIC interpolation-  This method is one of the best for preserving image quality during resizing, 
        as it considers the intensity values of neighboring pixels and uses polynomial interpolation to generate the
        new pixel value, resulting in a smoother and higher quality image compared to other methods.

        4. Normalization The images are then normalized to values between [-1,1] by subtracting and then dividing by 127,
         centering them around 0 (normalized this way for compatibility with created unet structure)

        5. Generate mask: The model is used to predict the binary mask based on the preprocessed image. Mask is then converted into
        appropriate datatype (from false/true to 0/1) and rescaled to [0,255] range (uint8) for compatibility with original image.

        6. Apply mask: The 'cv2.bitwise_and' function performs a bitwise AND operation between the original image and the mask. 
        Since the mask contains only 0s and 1s, this operation effectively preserves the pixel values where the mask is 1 
        and sets the pixel values to 0 where the mask is 0. The result is an image
        where the regions corresponding to the mask are preserved and the rest of the image is set to black.

        TO INVESTIGATE: converting image to grayscale seems to be thesholding the image a little bit, causing brigther image.
        Also it seems that resulting masked image is darker when not converted to grayscale. Investigate further.
    """
    threshold = float(threshold)  # for safety reasons

    # * This segment basically preprocesses the image for segmentation. THis can be included in crop image,
    # * but for now, we are doing it here for clarity that this is purely and specially for segmentation process only
    # Save the original image for display later
    orig_img = image
    # Convert to float32 before normalization to get better floating point precision
    image = image.astype(np.float32)
    image = (image - threshold) / threshold
    print(
        "Original image pixel statistics after preprocessing (shape, min,max,mean): ",
        image.shape,
        image.min(),
        image.max(),
        image.mean(),
    )

    # This is the segment that segments the image.
    # 0.9 ensures that mask is more sensitive to edges, ensures mask is only 0 or values close to 1
    mask_result = model.predict(np.expand_dims(image, axis=0))[0] > 0.9
    print(
        "mask_result shape straight after prediction (size, min,max,mean): ",
        mask_result.shape,
        mask_result.min(),
        mask_result.max(),
        mask_result.mean(),
    )

    mask_rescaled = (mask_result).astype(np.uint8)
    print(
        "\nmask result after being rescaled for compatibility with original image then its mean(turn boolean values to 0/1) ",
        mask_rescaled.shape,
        mask_rescaled.min(),
        mask_rescaled.max(),
        mask_rescaled.mean(),
    )
    # Application of the created mask onto the original image to isolate the lungs itself
    masked_image = cv2.bitwise_and(orig_img, orig_img, mask=mask_rescaled)

    print(
        f"\nOrig image data: {orig_img.shape} | {orig_img.dtype} |",
        f"original image values (min,max, mean): {np.min(orig_img), np.max(orig_img), np.mean(orig_img)} ",
    )

    print(
        f"Masked image data: {masked_image.shape} | {masked_image.dtype} |",
        f"masked image values (min,max, mean): {np.min(masked_image), np.max(masked_image), np.mean(masked_image)}",
    )

    print(
        f"mask_result image data: {mask_result.shape} | {mask_result.dtype} |",
        f"mask image values (min,max, mean): {np.min(mask_result), np.max(mask_result), np.mean(mask_result)}",
    )
    print("\n---End of Segmentation---\n\n")

    return orig_img, masked_image, mask_result


# -----END OF SEGMENTATION PROCESS-----#

# -----START CLASSIFICATION PROCESS-----#


def classify_image(model, image, img_shape=(512, 512)):
    print("\n\n---Start of Classification---\n")
    """
    Classifies an image using a given model.

    Parameters:
        model (keras.Model): The pre-trained model used for classification.
        image (numpy.ndarray): The input image to be classified.
        img_shape (tuple): The desired shape of the image (default: (512, 512)).

    Returns:
        tuple: A tuple containing the classification result and the predicted score.
            - classification (str): The classification result, either "Tuberculosis" or "Non-Tuberculosis".
            - predicted_score_rounded (float): The predicted score rounded to two decimal places.
    """

    # image = cv2.resize(image, img_shape, interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    img_afterRGB = image  # ?Just to see, remobable sa future
    # image = keras.applications.resnet.preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    print(
        "Preproccesed Image straight after segmentation (type, size, min , max, mean)",
        image.dtype,
        image.shape,
        image.min(),
        image.max(),
        image.mean(),
    )

    prediction = model.predict(image)
    if prediction[0][0] > 0.5:
        # print("Tuberculosis ")
        classification = "Tuberculosis"
    else:
        # print("Non-Tuberculosis")
        classification = "Non-Tuberculosis"

    print(f"{prediction[0][0]} is the original score")

    predicted_score_rounded = round((prediction[0][0] * 100.0), 2)
    raw = prediction[0][0]

    print(
        f"{prediction[0][0]}  rounded: {predicted_score_rounded}  then raw {raw}: test if raw score was changed after rounding to 2 decimal places"
    )

    print("\n\n---End of Classification---\n")
    return classification, predicted_score_rounded, raw


# -----END OF CLASSIFICATION PROCESS-----#


# -----GRADCAM SECTION-----#
def make_gradcam_heatmap(image, model, last_conv_layer_name = last_conv_layer_name, pred_index=None):
    print("\n\n---Start of creating gradCAM---\n")

    # * This segment contains the simple preprocessing of the image for creating the gradCAM heatmap
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = np.expand_dims(image, axis=0)

    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(image)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]
    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

    print("\n\n---End  of creating gradCAM---\n")
    return heatmap.numpy()


def superimpose_heatmap(original_img, heatmap, alpha=0.4):
    print("\n\n---Start of Superimposing image---\n")

    # Load the original image
    # img = keras.utils.load_img(original_img, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH, 3))
    # img = keras.utils.img_to_array(img)

    original_img = cv2.cvtColor(original_img, cv2.COLOR_GRAY2RGB)

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

    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.utils.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((original_img.shape[1], original_img.shape[0]))
    jet_heatmap = keras.utils.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + original_img
    superimposed_img = keras.utils.array_to_img(superimposed_img)

    # Save the superimposed image
    # superimposed_img.save(cam_path)

    # Display Grad CAM
    # display(Image(cam_path))

    print("\n\n---End of superimposing image---\n")
    return superimposed_img

#! Experimental, this process attempts to overlay heatmap in the shape of the segmented image,
#! onto original image
def superimpose_heatmap_V3(original_img, segmented_img, heatmap, alpha=0.3):
    """
    Superimposes the heatmap onto the original image, restricted to the regions defined by the segmented image.

    Args:
        original_img (numpy.ndarray): The original image.
        segmented_img (numpy.ndarray): The segmented image defining the regions of interest.
        heatmap (numpy.ndarray): The heatmap to be superimposed.
        alpha (float, optional): The blending factor for the heatmap. Defaults to 0.4.

    Returns:
        "Image" object: The superimposed image.
    """
    # original_img = cv2.cvtColor(original_img, cv2.COLOR_GRAY2RGB)

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

    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.utils.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((original_img.shape[1], original_img.shape[0]))
    jet_heatmap = keras.utils.img_to_array(jet_heatmap)

    # Convert segmented image to binary mask
    binary_mask = (segmented_img > 0).astype(np.uint8)

    # Expand dimensions of binary mask to match the number of channels in the heatmap
    # binary_mask_expanded = np.expand_dims(binary_mask, axis=-1)

    # Superimpose the heatmap onto the original image
    # superimposed_img = jet_heatmap * binary_mask_expanded + original_img * (1 - binary_mask_expanded)
    # superimposed_img = jet_heatmap * binary_mask + original_img * (1 - binary_mask)
    superimposed_img = jet_heatmap * binary_mask 

    # Convert the superimposed image back to uint8
    superimposed_img = superimposed_img.astype(np.uint8)

    return superimposed_img

#! Experimental, All in one generate heatmap, then overlay heatmap onto original image
def get_gradCAM(model_classifier, original_image, masked_image):
    # Remove last layer's activatio
    model_classifier.layers[-1].activation = None

    # preprocessed_img = get_img_array(masked_image)

    # Generate Grad-CAM heatmap (replace arguments with actual values)
    heatmap = make_gradcam_heatmap(
        masked_image, model_classifier, last_conv_layer_name
    )

    orig_temp = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)
    masked_temp = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2RGB)

    superimposed_segmented_onto_whole_img = superimpose_heatmap_V3(
        orig_temp, masked_temp, heatmap
    )
    # activating again the classifier
    model_classifier.layers[-1].activation = tf.keras.activations.sigmoid

    # superimposed_img = cv2.resize(superimposed_img, (512, 512))

    return superimposed_segmented_onto_whole_img


# ----END OF GRADCAM SECTION----#

# ----- SAMPLE SECTION TO RUN BASIC FLOW OF APP
# ? CHECKING IF EVERYTHING WORKS/ PLEASE UNCOMMENT OR COMMENT ACCORDINGLY


# def run_sample (MAIN_IMG_PATH, model_unet, model_efficientnet):# * Checking image
#     faulty_img = check_image(MAIN_IMG_PATH)

#     if not faulty_img:
#         # * Cropping and resizing image
#         cropped_img = crop_resize_image(MAIN_IMG_PATH)

#         # * Segmentation part
#         original_image, masked_image, mask_result = segment_imageV2(
#             model_unet,
#             cropped_img,
#             img_shape=(512, 512),
#             threshold=120,
#         )

#         # * Check if segmentation is successful
#         segment_bad = check_segmented_img(masked_image, mask_result)

#         if not segment_bad:
#             # * Classification part
#             classification, score, raw = classify_image(model_efficientnet, masked_image)

#             # * GradCAM part, do not include Cl;assification ==Non tuberculosis if want to mimic actual flow of program
#             if classification == "Tuberculosis" or classification == "Non-Tuberculosis":
#                 # ? genearte gradcam of segmented image, but superimpose it onto original img (not yet cropped)
#                 heatmap = make_gradcam_heatmap(
#                     masked_image, model_efficientnet, last_conv_layer_name
#                 )
#                 print(f"heatmap shape and datatype: {heatmap.shape} | {heatmap.dtype}")
#                 superimposed_img = superimpose_heatmap(original_image, heatmap)

#                 # ? to test if model, trained on segmented images, what it sees if whole image is processed
#                 heatmap_wholeimg = make_gradcam_heatmap(
#                     original_image, model_efficientnet, last_conv_layer_name
#                 )
#                 superimposed_img_wholeimg = superimpose_heatmap(
#                     original_image, heatmap_wholeimg
#                 )

#                 # ? generate gradcam on segmented image
#                 superimposed_img_onsegmented = superimpose_heatmap(masked_image, heatmap)

#                 # ? Final wanted output, overlay only the shape of the segmented image, onto original image, then heatmap
#                 super_superimposed_img = get_gradCAM (model_efficientnet, original_image, masked_image)

#             else:
#                 # If want to mimic actual process or flow of program, uncomment next line
#                 # superimposed_img , superimposed_img_wholeimg, superimposed_img_onsegmented = mask_result, mask_result, mask_result  # produced mask image, no idea how to implement pa i2
#                 pass

#             # Following code are not necessary, just for checking purposes
#             print(f"Classification: {classification} | Score: {score} | Raw: {raw}")

#             fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(
#                 2, 4, figsize=(20, 10)
#             )

#             im = cv2.imread(MAIN_IMG_PATH)
#             print(
#                 "\nOriginal, unprocessed image shape: ",
#                 im.shape,
#                 im.dtype,
#                 im.min(),
#                 im.max(),
#                 im.mean(),
#             )

#             # Display the original image, that was preprocessed by system and not "the original image"
#             ax1.imshow(original_image, cmap="gray")
#             ax1.set_title("CUSTOM IMAGE FILE")
#             ax1.axis("off")

#             # Display the masked imh
#             ax2.imshow(masked_image, cmap="gray")
#             ax2.set_title("Masked image")
#             ax2.axis("off")

#             # Display the masked image
#             ax3.imshow(mask_result, cmap="gray")
#             ax3.set_title("Mask result")
#             ax3.axis("off")

#             # genearte heatmap of segmented image, but superimpose it onto original img (not yet cropped)
#             ax4.imshow(superimposed_img)
#             ax4.set_title(f"GradCAM of segmented onto whole,\n rawscore: {raw:.1f}")
#             ax4.axis("off")

#             # generate gradcam on segmented image, then apply onto segmented imaage itself
#             ax5.imshow(superimposed_img_onsegmented)
#             ax5.set_title("GradCAM segmented img only")
#             ax5.axis("off")

#             # generate heatmap by scanning the whole image and then producing heatmap on it
#             ax6.imshow(superimposed_img_wholeimg)
#             ax6.set_title("GradCAM on whole image")
#             ax6.axis("off")

#             # TESTING FOR NOW
#             ax7.imshow(super_superimposed_img)
#             ax7.set_title("Final wanted output\nEXPERIMENTAL")
#             ax7.axis("off")

#             # You can use ax8 for another plot or just hide it if not needed
#             ax8.axis("off")

#             # Adjust the spacing between subplots
#             plt.subplots_adjust(wspace=0.1)

#             # Show the plot
#             plt.show()

#         else:
#             print("Segmentation failed. Please check the image.")

#     else:
#         print("Image is faulty at input. Please check the image.")


# model_unet = load_model_unet(r"assets\ml-model\unet_V0_1_7.h5")
# model_efficientnet = load_model_efficientNet(r"assets\ml-model\efficientnetB3_V0_7_11.h5")
# SAMPLE_IMG_TEST = r"assets\sample-images\Normal-3499.png"
# run_sample(SAMPLE_IMG_TEST, model_unet, model_efficientnet)
