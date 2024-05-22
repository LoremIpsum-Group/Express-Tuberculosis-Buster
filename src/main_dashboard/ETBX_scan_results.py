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

#Load the trained model
model_classifier = load_model_efficientNet('assets/ml-model/efficientnetB3_V0_6_1.h5')
model_segmentation = load_model_unet('assets/ml-model/unet_V0_1_3.h5')

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_res.kv")

class ScanResult(Screen):
    def update_result(self, image_path):
        global xrayRes
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
        if instance == self.ids.x_ray:
            self.ids.res_img.source = xrayRes
        elif instance == self.ids.grad_cam:
            #dummy
            self.ids.res_img.source = 'assets/heat.png'
        elif instance == self.ids.pre_proc: 
            #dummy
            self.ids.res_img.source = 'assets/xray.jpg'        
        else:
            pass