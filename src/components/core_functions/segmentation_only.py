from components.core_functions.dependencies_loading import (
    tf,
    np,
    cv2,
    plt,
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    last_conv_layer_name,
    load_model,
)

def segment_image(model, path, img_shape=(512, 512), threshold=0.5):
    """
    Segment an image using a segmentation model.

    **********Input**************
    model: segmentation model (h5)
    path: filepath to the image (string)
    img_shape: shape of the image (IMG_WIDTH, IMG_HEIGHT) used in the segmentation model (default: (512, 512))
    threshold: float value between 0 and 1 for thresholding the mask (default: 0.5)

    *********Output*************
    Returns a tuple containing:
        - Original image: The resized grayscale image before segmentation
        - Masked image: The original image after applying the segmentation mask
        - Segment mask: The binary segmentation mask obtained from the model
    """

    IMG_WIDTH, IMG_HEIGHT = img_shape
    chest_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    chest_image = cv2.resize(chest_image, (IMG_HEIGHT, IMG_WIDTH))

    # chest_image = chest_image/255.0
    chest_image = chest_image.astype(np.float32)
    # chest_image = np.expand_dims(chest_image, axis=0)

    im_array_temp = []

    # get specific channel from image (first channel)
    im = cv2.resize(cv2.imread(path), (IMG_HEIGHT, IMG_WIDTH))[:, :, 0]
    im_array_temp.append(im)

    # Reshape im_array and mask_array directly
    im_array_temp = np.array(im_array_temp).reshape(
        len(im_array_temp), IMG_HEIGHT, IMG_WIDTH, 1
    )

    im_array_temp = (im_array_temp - 127.0) / 127.0
    # im_array_temp = (im_array_temp / 255.0)

    y_pred = model.predict(im_array_temp)[0] > threshold
    y_pred = y_pred.astype(np.float32)

    mask_result = np.squeeze(y_pred)
    chest_image = cv2.resize(
        chest_image, (IMG_HEIGHT, IMG_WIDTH), interpolation=cv2.INTER_NEAREST
    )

    masked_image = chest_image * mask_result

    return chest_image, masked_image, mask_result
