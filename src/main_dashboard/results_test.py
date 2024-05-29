from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder

import sqlite3 
import io
from PIL import Image

Builder.load_file('src/main_dashboard/resultstest.kv')
class ResultsTest(Screen):
    def __init__(self, **kwargs):
        self.exists_layout = False
        self.not_exists_layout = False
        super().__init__(**kwargs)

    def exists(self):
        self.ids.patient_search_result.clear_widgets()
        patient_info_content1 = BoxLayout(orientation='horizontal')
        name_label = Label(text='Name: ', color=(0,0,0,1))
        age_label = Label(text='Age: ', color=(0,0,0,1))
        patient_info_content1.add_widget(name_label)
        patient_info_content1.add_widget(age_label)

        patient_info_content2 = BoxLayout(orientation='horizontal')
        sex_label = Label(text='Sex:\nMale ', color=(0,0,0,1))
        birthdate_label = Label(text='Birthdate: ', color=(0,0,0,1))
        patient_info_content2.add_widget(sex_label)
        patient_info_content2.add_widget(birthdate_label)

        self.ids.patient_search_result.add_widget(patient_info_content1)
        self.ids.patient_search_result.add_widget(patient_info_content2)
    
    def not_exists(self):
        self.ids.patient_search_result.clear_widgets()
        self.ids.patient_search_result.add_widget(Label(
            text="No Patient Found! Please check the Patient ID and try again.",
            color=(1,0,0,1)
        ))



    def search_result(self):
        result_id = self.ids.result_id.text
        connection = sqlite3.connect('src/components/view_record_main.db')
        cursor = connection.cursor()
        cursor.execute("SELECT orig_image, preproc_image, grad_cam_image FROM RESULTS WHERE result_id = ?", (int(result_id),))
        result_data = cursor.fetchone()

        if result_data is None:
            print("No result found")
        else:
            orig_image_bytes = result_data[0]
            orig_image_stream = io.BytesIO(orig_image_bytes)
            orig_image = Image.open(orig_image_stream)
            orig_image.save('orig_image.jpg')
            orig_img = 'orig_image.jpg'

            preproc_image_bytes = result_data[1]
            preproc_image_stream = io.BytesIO(preproc_image_bytes)
            preproc_image = Image.open(preproc_image_stream)
            preproc_image.save('preproc_image.jpg')
            preproc_img = 'preproc_image.jpg'

            gradcam_image_bytes = result_data[2]
            gradcam_image_stream = io.BytesIO(gradcam_image_bytes)
            gradcam_image = Image.open(gradcam_image_stream)
            gradcam_image.save('gradcam_image.jpg')
            gradcam_img = 'gradcam_image.jpg'

            print("Result Found")
            self.ids.orig_image.source = orig_img
            self.ids.preproc_image.source = preproc_img
            self.ids.gradcam_image.source = gradcam_img
        
class ResultsTestApp(App):

    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(ResultsTest(name='results_test'))
        return self.screen_manager


ResultsTestApp().run()