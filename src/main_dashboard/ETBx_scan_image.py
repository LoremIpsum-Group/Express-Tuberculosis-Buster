from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_img.kv")
class ScanImage(Screen):
    pass


# import tkinter as tk
# from tkinter import filedialog
# from kivy.app import App 
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import Image
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.utils import platform
# from components.classifier_only import load_model_from_file, predict

# # Load the trained model
# model = load_model_from_file('assets\ml-model\efficientNetB7_v0-5.h5')

# class ETBX_scan_image(App):
#     def build(self):

#         #main layout
#         self.layout = BoxLayout(orientation='horizontal')

#         #box kung san paglalagyan image and texts
#         full_layout = BoxLayout(orientation = 'vertical')
#         self.image = Image()
#         full_layout.add_widget(self.image)

#         #textboxes para sa result, di alam san pwede ilagay grad cam image.
#         self.result_class = Label(text="Class Result", size_hint_y=None, height=50)
#         full_layout.add_widget(self.result_class)
#         self.result_perc = Label(text="Percentage", size_hint_y = None, height=50)
#         full_layout.add_widget(self.result_perc)

#         #buttons, upload para preview tapos process for the thingy. 
#         buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height = 50)
#         self.upload_button = Button(text="Upload Image", size_hint_y=None, height=50)
#         self.upload_button.bind(on_press=self.load_image)
#         buttons_layout.add_widget(self.upload_button)

#         self.process_button = Button(text="Process Image", size_hint_y=None, height=50)
#         self.process_button.bind(on_press=self.process_image)
#         buttons_layout.add_widget(self.process_button)

#         full_layout.add_widget(buttons_layout)
#         self.layout.add_widget(full_layout)

#         return self.layout

#     #pindot upload image mag-gogo to, tapos display image
#     def load_image(self, instance):
#         file_path = self.file_dialog()
#         if file_path:
#             self.put_image(file_path)

#     def file_dialog(self):
#         root = tk.Tk()
#         root.withdraw()  
#         file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
#         root.destroy()  
#         return file_path

#     def put_image(self, file_path):
#         if file_path:
#             self.image.source = file_path

#     #pindot process mag-gogo to, tapos display result. 
#     def process_image(self, instance):
#         # Path to the image you want to predict on
#         image_path = self.image.source

#         # Make predictions
#         predicted_class, predicted_score = predict(model, image_path)

#         # Print the predicted class label and score
#         #print("Predicted Class:", predicted_class)
#         #print("Predicted Score:", predicted_score)
#         #print("Full score:", predicted_score_full)
        
#         scoree = float(predicted_score) * 100
#         #self.result_class.text = "TestTest " 
#         #self.result_perc.text = "Test " 
#         self.result_class.text = "Predicted Class: " + predicted_class
#         self.result_perc.text = "Predicted Score: " + str(scoree) + " %"
#         pass

# if __name__ == "__main__":
#     ETBX_scan_image().run()
