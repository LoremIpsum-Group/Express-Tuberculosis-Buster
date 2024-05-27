
import sqlite3, base64, io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np



def img_string(image):
    """
    Changes the displayed image based on the selected instance. In-depth procedure:
    1. Save PIL Image to BytesIO object. A BytesIO object is like a file object, but it resides in memory instead of being saved to disk.
    2. Retrieve the contents of the BytesIO object as a bytes string using the `getvalue` method.
    3. Encode the bytes string into base64 format. Base64 encoding is a way of converting binary data into text format, which is needed because `img.source` expects a string.
    4. Convert the string into a data URL by adding the prefix 'data:image/png;base64,'. A data URL is a URI scheme that allows you to include data in-line in web pages as if they were external resources.
    """
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        contents = output.getvalue()

    img_data = base64.b64encode(contents).decode('ascii')
    return 'data:image/png;base64,' + img_data 

 
def update_result(res_id):
    """
    Updates the scan result with the provided image path.

    Args:
        image_path (str): The path to the image file.

    Returns:
        None
    """
    conn = sqlite3.connect('src/components/view_record_main.db')
    c = conn.cursor()
    c.execute("SELECT orig_image, preproc_image, grad_cam_image, percentage, notes FROM RESULTS WHERE patient_id = ?", (res_id,))
    result = c.fetchone()



    orig_image_bytes = result[0]
    orig_image_stream = io.BytesIO(orig_image_bytes)
    orig_image = Image.open(orig_image_stream)

    orig_image_string = img_string(orig_image)
    # orig_image.save('orig_image.jpg')            
    # orig_img = 'orig_image.jpg'
    #assets/temp-img-location-per-view-records/

    #temp = CoreImage(orig_image_stream, ext)
    
    print(type(orig_image_bytes))
    print(type(orig_image_stream))
    print(type(orig_image))
    print(orig_image_string)
    #orig_converted = orig_image.astype(np.uint8)
    

    
    # plt.imshow(orig_image)
    # plt.axis('off')
    # plt.show()
    #preproc_image_bytes = self.img_string(result[1])
    # preproc_image_stream = io.BytesIO(preproc_image_bytes)
    # preproc_image = Image.open(preproc_image_stream)
    # preproc_image.save('preproc_image.jpg')
    # preproc_img = 'preproc_image.jpg'

    #gradcam_image_bytes = self.img_string(result[2])
    # gradcam_image_stream = io.BytesIO(gradcam_image_bytes)
    # gradcam_image = Image.open(gradcam_image_stream)
    # gradcam_image.save('gradcam_image.jpg')
    # gradcam_img = 'gradcam_image.jpg'

    percent = result[3]

    note = result[4]

    #print(type(gradcam_image_bytes))
    #print(type(preproc_image_bytes))

update_result('5481')