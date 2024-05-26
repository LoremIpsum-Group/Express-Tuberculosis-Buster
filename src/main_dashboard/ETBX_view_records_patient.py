from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton   
from kivy.properties import NumericProperty
from main_dashboard.ETBX_full_view import xray_full_app



from components.core_functions import (
    load_model_efficientNet,
    load_model_unet,
    segment_image,
    predict,
    get_gradCAM,
    sqlite3,
    io,
    plt,
    np,
    Image,
    base64
)

class ScanResultData: 
    """
        A class that stores information about results of scanned X-ray 
        for database storage 
    """

    def __init__(self):
        self.results = None 
        self.percentage = None 
        self.orig_img = None 
        self.preproc_img = None
        self.gradcam_img = None 
        self.notes = None 

scan_result = ScanResultData() 

# Load the trained model
model_classifier = load_model_efficientNet('assets/ml-model/efficientnetB3_V0_6_1.h5')
model_segmentation = load_model_unet('assets/ml-model/unet_V0_1_3.h5')

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_view_rcrds_patient.kv")

# scan_results = ScanResultData()
class PatientResult(Screen):
    """
    Represents a screen for displaying scan results.

    Attributes:
        None

    Methods:
        update_result(image_path): Updates the scan result with the provided image path.
        change_img(instance): Changes the displayed image based on the selected instance.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        c.execute(
            """ 
            CREATE TABLE IF NOT EXISTS RESULTS (
                result_id INTEGER PRIMARY KEY, 
                patient_id INTEGER, 
                date_of_scan TEXT NOT NULL, 
                result TEXT NOT NULL,
                percentage REAL, 
                orig_image BLOB NOT NULL, 
                preproc_image BLOB NOT NULL, 
                grad_cam_image BLOB NOT NULL, 
                notes TEXT, 
                FOREIGN KEY(patient_id) REFERENCES PATIENT(patient_id)
            )
        """
        )
        
        # working table but keeps on adding
        # c.execute("""CREATE TABLE IF NOT EXISTS main_table (  
        #         result_ID INTEGER NOT NULL,
        #         patient_ID INTEGER NOT NULL,
        #         date_of_scan TEXT NOT NULL,
        #         result TEXT NOT NULL, 
        #         percentage TEXT NOT NULL)
        #         """)
     
        conn.commit()
        conn.close()

       

    def img_string(self, image):
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
    
    def update_result(self, image_blob):
        """
        Updates the scan result with the provided image path.

        Args:
            image_path (str): The path to the image file.

        Returns:
            None
        """
        def save_image_from_bytes(image_bytes, file_path):
            image = Image.open(io.BytesIO(image_bytes))
            image.save(file_path)

        image_bytes = bytes(image_blob)

        image = Image.open(io.BytesIO(image_bytes))

        global xray_orig, xray_orig_resized, superimposed_img, masked_image
        xray_orig = image

        file_path = "assets/temp-img-location-per-view-records/view_record_temp.png"

        #assets/temp-img-location-per-view-records
        save_image_from_bytes(xray_orig, file_path)


        self.ids.res_img.source = xray_orig
        self.ids.x_ray.md_bg_color = (0.1, 0.5, .9, 1)
        self.ids.x_ray.text_color = (1, 1, 1, 1)

        # !CORE FUNCTIONALITIES - START
        # Get segmented/masked image
        xray_orig_resized, masked_image, mask_result = segment_image(
             model_segmentation, xray_orig
        )

        # Get Score from segmented image
        predicted_class, predicted_score = predict(model_classifier, masked_image)

        # Superimpose heatmap of segmented image onto original image
        superimposed_img = get_gradCAM(model_classifier, xray_orig_resized, masked_image)

        # !CORE FUNCTIONALITIES - end
        # *DEBUGGING PURPOSES, removable any time
        # preprocessed_img = get_img_array_OLD(masked_image)
        # predicted_class, predicted_score = predict(model_classifier, preprocessed_img)
        # superimposed_img = get_gradCAM_NONSEGMENTED(model_classifier, original_image)
        # * Replace here the image you want to display, temporary ONLY!!!!!
        # Good results: normal 2551, tuberculosis 640

        # plt.imshow(superimposed_img)
        # plt.axis('off')  # Turn off axis
        # plt.show()

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

        scan_result.results = predicted_class
        scan_result.percentage = predicted_score
        scan_result.orig_img = xray_orig
        scan_result.preproc_img = masked_image 
        scan_result.gradcam_img = superimposed_img
        scan_result.notes = self.ids.notes.text

    def change_img(self, instance):
        white = (1, 1, 1, 1)  # Default color
        blue = (0.1, 0.5, .9, 1)  # Pressed color

        # Reset all buttons to default color
        self.ids.x_ray.md_bg_color = white
        self.ids.x_ray.text_color = blue
        self.ids.pre_proc.md_bg_color = white
        self.ids.pre_proc.text_color = blue
        self.ids.grad_cam.md_bg_color = white
        self.ids.grad_cam.text_color = blue

        # Change the pressed button's color
        instance.md_bg_color = blue
        instance.text_color = white

        if instance == self.ids.x_ray:
            self.ids.res_img.source = xray_orig

        elif instance == self.ids.grad_cam:
            img = Image.fromarray((superimposed_img) .astype(np.uint8))
            #img = img.convert("RGB")            
                     
            self.ids.res_img.source = self.img_string(img)   

        elif instance == self.ids.pre_proc: 
            img = Image.fromarray(((1.0 - masked_image) * 255).astype(np.uint8))
            img = img.convert('L')

            self.ids.res_img.source = self.img_string(img) 

        else:
            pass


    def full_view(self):
        xrayPath = xray_orig
        supIM = superimposed_img

        xray_full_app(xrayPath, supIM)
        pass
