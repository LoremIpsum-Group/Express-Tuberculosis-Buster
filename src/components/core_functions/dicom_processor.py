from components.core_functions.dependencies_loading import (
    Image, 
    cv2,
    pydicom,
    np
)


def extract_image(dicom_path): 
    """
        Extracts image array from a dicom file 
    """

    dicom = pydicom.dcmread(dicom_path)
    raw_pixel = dicom.pixel_array # get image array

    # convert to 8-bit image
    img = cv2.convertScaleAbs(raw_pixel, alpha=(255.0/raw_pixel.max()))
    if len(img.shape) == 2:
        img = cv2.equalizeHist(img)
        img = Image.fromarray(img)
        img = img.convert('RGB') 
        img = np.array(img)

    return img 

