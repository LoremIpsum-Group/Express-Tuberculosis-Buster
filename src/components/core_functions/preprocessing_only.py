from components.core_functions.dependencies_loading import (
    os,
    keras,
    tf,
    np,
    cv2,
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
)

def get_img_array_OLD(img_holder, size=(IMAGE_HEIGHT, IMAGE_WIDTH, 3)):
    if os.path.isfile(img_holder):
        img = tf.keras.preprocessing.image.load_img(img_holder, target_size=size)

    else:
        img = cv2.resize(img_holder, (size[0], size[1]))  # Resize to desired size

    array = tf.keras.preprocessing.image.img_to_array(img)
    # We add a dimension to transform our array into a "batch"
    # of size "size"
    array = np.expand_dims(array, axis=0)
    return array


# Only used in superimposing the heatmap onto the original image
def get_img_array_original(img_holder):
    if os.path.isfile(img_holder):
        # Load the original image
        img = keras.utils.load_img(img_holder, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH, 3))
        array = keras.utils.img_to_array(img)
        return array
    
    else:
        print("File not file path!")


##### SECTION FOR WHEN IMAGE BEING PROCESSED IS NOW A SEGMENTED IMAGE


'''
Used in segmentation, to prepare segmented image (greyscale) for the model (expects rgb channels)
to be revised once classifier model now fine tuned for greyscale
'''

def get_img_array(img_holder, size=(IMAGE_HEIGHT, IMAGE_WIDTH)):
    if os.path.isfile(img_holder):
        img = tf.keras.preprocessing.image.load_img(
            img_holder, color_mode="grayscale", target_size=size
        )
    else:
        img = cv2.resize(
            img_holder, (size[1], size[0]), interpolation=cv2.INTER_NEAREST
        )
    # ONly because classifier model expects image with rgb channel and not grayscale. remove in the future
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    array = tf.keras.preprocessing.image.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return array


'''
 Becasue the efficientnetmodelB3 expects the inpuits to be RGB channel, resizing of 
the original image along with the masked image happens here. Will be refactored.
Function used for superimposing the generated heatmap from the segmented image
into the original, whole img
'''
def temporary_process (original_img, masked_img):
    # TEMPORARY PREPROCESSING THE ORIGINAL IMAGE THAT WAS OUTPUTTED BY SGMENTATION MODEL
    original_preprocessed = cv2.cvtColor(original_img, cv2.COLOR_GRAY2RGB)
    original_preprocessed = cv2.resize(
        original_preprocessed,
        (IMAGE_WIDTH, IMAGE_HEIGHT),
        interpolation=cv2.INTER_NEAREST,
    )

    # TEMPORARY PREPROCESSING THE SEGMENTED IMAGE THAT WAS OUTPUTTED BY SGMENTATION MODEL
    masked_preprocessed = cv2.cvtColor(masked_img, cv2.COLOR_GRAY2RGB)
    masked_preprocessed = cv2.resize(
        masked_preprocessed,
        (IMAGE_WIDTH, IMAGE_HEIGHT),
        interpolation=cv2.INTER_NEAREST,
    )

    return original_preprocessed, masked_preprocessed
