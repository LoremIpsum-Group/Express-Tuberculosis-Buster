from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton   
from kivy.properties import NumericProperty

from components.core_functions.load_models import load_model_efficientNet, load_model_unet
from components.core_functions.preprocessing_only import get_img_array, get_img_array_OLD


from components.core_functions.segmentation_only import segment_image
from components.core_functions.classifier_only import predict
from components.core_functions.grad_CAM_new import get_gradCAM, get_gradCAM_NONSEGMENTED

import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from PIL import Image

#Load the trained model
model_classifier = load_model_efficientNet('assets/ml-model/efficientnetB3_V0_6_1.h5')
model_segmentation = load_model_unet('assets/ml-model/unet_V0_1_3.h5')

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_res.kv")

class ScanResult(Screen):
    """
    Represents a screen for displaying scan results.

    Attributes:
        None

    Methods:
        update_result(image_path): Updates the scan result with the provided image path.
        change_img(instance): Changes the displayed image based on the selected instance.
    """

    def update_result(self, image_path):
        """
        Updates the scan result with the provided image path.

        Args:
            image_path (str): The path to the image file.

        Returns:
            None
        """
        global xrayRes, superimposed_img, masked_image
        xrayRes = image_path
        self.ids.res_img.source = xrayRes

        # !CORE FUNCTIONALITIES - START
        # Get segmented/masked image
        original_image, masked_image, mask_result = segment_image(
             model_segmentation, image_path
        )

        # Get Score from segmented image
        predicted_class, predicted_score = predict(model_classifier, masked_image)

        # Superimpose heatmap of segmented image onto original image
        superimposed_img = get_gradCAM(model_classifier, original_image, masked_image)

        # !CORE FUNCTIONALITIES - end
        # *DEBUGGING PURPOSES, removable any time
        # preprocessed_img = get_img_array_OLD(masked_image)
        # predicted_class, predicted_score = predict(model_classifier, preprocessed_img)
        # superimposed_img = get_gradCAM_NONSEGMENTED(model_classifier, original_image)
        # * Replace here the image you want to display, temporary ONLY!!!!!
        # Good results: normal 2551, tuberculosis 640

        plt.imshow(superimposed_img)
        plt.axis('off')  # Turn off axis
        plt.show()

        bar_color = None
        if (predicted_score <= 25):
            bar_color = (0, 1, 0, 1)
        elif (predicted_score <= 49):
            bar_color = (1, 1, 0, 1)
        elif (predicted_score <= 74):
            bar_color = (1, 0.5, 0, 1)
        else:
            bar_color = (1, 0, 0, 1)

        self.percentage = int(predicted_score)
        self.percentage_color = bar_color
        self.ids.result_classnPerc.text = predicted_class + ": " +str(predicted_score) + " %\n segmented datatype: " + str(masked_image.dtype)

    def change_img(self, instance):
        """
        Changes the displayed image based on the selected instance. In-depth procedure:
        1. Convert numpy array to PIL Image.
        2. Reorder color channels.
        3. Save PIL Image to BytesIO object. A BytesIO object is like a file object, but it resides in memory instead of being saved to disk.
        4. Retrieve the contents of the BytesIO object as a bytes string using the `getvalue` method.
        5. Encode the bytes string into base64 format. Base64 encoding is a way of converting binary data into text format, which is needed because `img.source` expects a string.
        6. Convert the string into a data URL by adding the prefix 'data:image/png;base64,'. A data URL is a URI scheme that allows you to include data in-line in web pages as if they were external resources.
        """
        if instance == self.ids.x_ray:
            self.ids.res_img.source = xrayRes

        elif instance == self.ids.grad_cam:
            img = Image.fromarray(((1.0 - superimposed_img) * 255).astype(np.uint8))
            img = img.convert("RGB")

            with io.BytesIO() as output:
                img.save(output, format="PNG")
                contents = output.getvalue()

            img_data = base64.b64encode(contents).decode('ascii')          
            self.ids.res_img.source = 'data:image/png;base64,' + img_data

        elif instance == self.ids.pre_proc: 
            img = Image.fromarray(((1.0 - masked_image) * 255).astype(np.uint8))
            img = img.convert('L')

            with io.BytesIO() as output:
                img.save(output, format="PNG")
                contents = output.getvalue()

            img_data = base64.b64encode(contents).decode('ascii')
            self.ids.res_img.source = 'data:image/png;base64,' + img_data     

        else:
            pass
