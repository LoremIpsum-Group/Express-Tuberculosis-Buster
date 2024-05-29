from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton   
from kivy.properties import NumericProperty
from main_dashboard.ETBX_full_view import xray_full_app



from components.core_functions import (

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
        img_string_bytes(image): Converts the image to a base64-encoded data URL.
        full_view(): Displays the full view of the scan result images.
    """
    def on_enter(self, *args):
        self.change_img(self.ids.x_ray)
        
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
                misclassified BOOLEAN,
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

    def img_string_bytes(self, image):
        """
        Changes the displayed image based on the selected instance. In-depth procedure:
        1. Save PIL Image to BytesIO object. A BytesIO object is like a file object, but it resides in memory instead of being saved to disk.
        2. Retrieve the contents of the BytesIO object as a bytes string using the `getvalue` method.
        3. Encode the bytes string into base64 format. Base64 encoding is a way of converting binary data into text format, which is needed because `img.source` expects a string.
        4. Convert the string into a data URL by adding the prefix 'data:image/png;base64,'. A data URL is a URI scheme that allows you to include data in-line in web pages as if they were external resources.
        """

        image_stream = io.BytesIO(image)
        png_image_object = Image.open(image_stream)

        with io.BytesIO() as output:
            png_image_object.save(output, format="PNG")
            contents = output.getvalue()


        img_data = base64.b64encode(contents).decode('ascii')
        return 'data:image/png;base64,' + img_data 
    
 
    def update_result(self, res_id):
        """
        Updates the scan result with the provided image path.

        Args:
            image_path (str): The path to the image file.

        Returns:
            None
        """
        conn = sqlite3.connect('src/components/view_record_main.db')
        c = conn.cursor()
        

        c.execute("SELECT orig_image, preproc_image, grad_cam_image, percentage, notes, result, patient_ID FROM RESULTS WHERE result_id = ?", (res_id,))
        result = c.fetchone()

        global orig_img, preproc_img, gradcam_img, percent, note, orig_image_bytes, gradcam_image_bytes

        

        orig_image_bytes = result[0]
        orig_img = self.img_string_bytes(orig_image_bytes)

        preproc_image_bytes = result[1]
        preproc_img = self.img_string_bytes(preproc_image_bytes)

        gradcam_image_bytes = result[2]
        gradcam_img = self.img_string_bytes(gradcam_image_bytes)
        # orig_image_bytes = self.img_string(result[0])
        # orig_image_stream = io.BytesIO(orig_image_bytes)
        #orig_image = Image.open(orig_image_stream)
        # orig_image.save('orig_image.jpg')            
        # orig_img = 'orig_image.jpg'
        #assets/temp-img-location-per-view-records/
        
        #print(type(orig_image))


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

        classification = result[5]

        patient_id = result[6]
        #print(type(gradcam_image_bytes))
        #print(type(preproc_image_bytes))


        #self.ids.res_img.source = xray_orig
        self.ids.x_ray.md_bg_color = (0.1, 0.5, .9, 1)
        self.ids.x_ray.text_color = (1, 1, 1, 1)


        bar_color = None
        if (percent <= 25):
            bar_color = (0, 1, 0, 1)
        elif (percent <= 49):
            bar_color = (1, 1, 0, 1)
        elif (percent <= 74):
            bar_color = (1, 0.5, 0, 1)
        else:
            bar_color = (1, 0, 0, 1)

        self.percentage = int(percent)
        self.percentage_color = bar_color
        self.ids.result_classnPerc.text =  classification + ": " + str(percent)
        self.ids.patient_id_text.text = 'Scan Results for Patient: ' + str(patient_id)
        self.ids.notes.text = note

        # scan_result.percentage = percent
        # scan_result.orig_img = xray_orig
        # scan_result.preproc_img = masked_image 
        # scan_result.gradcam_img = superimposed_img
        # scan_result.notes = self.ids.note.text

    def change_img(self, instance):
        white = (1, 1, 1, 1)  # Default color
        blue = (0.1, 0.5, .9, 1)  # Pressed color

        self.ids.res_img.source = orig_img #open agad 

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
            self.ids.res_img.source = orig_img
            print(type(orig_img))
        elif instance == self.ids.grad_cam:            
            self.ids.res_img.source = gradcam_img 
            print(type(gradcam_img))
        elif instance == self.ids.pre_proc: 
            self.ids.res_img.source = preproc_img
            print(type(preproc_img))
        else:
            pass
    
    

    def full_view(self):
        #base64_decoded = base64.b64decode(orig_img)
        image = Image.open(io.BytesIO(orig_image_bytes))
        image_np_orig = np.array(image)

        #base64_decoded1 = base64.b64decode(gradcam_img)
        image1 = Image.open(io.BytesIO(gradcam_image_bytes))
        image_np_grad = np.array(image1)

      
        xray_full_app(image_np_orig, image_np_grad)
        pass
