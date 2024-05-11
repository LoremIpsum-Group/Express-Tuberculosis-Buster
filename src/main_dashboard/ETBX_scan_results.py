from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
#from components.classifier_only import load_model_from_file, predict

# Load the trained model
# model = load_model_from_file('assets\ml-model\efficientNetB7_v0-5.h5')

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_res.kv")

class ScanResult(Screen):
    # def update_result(self, image_path):
    #     self.ids.res_img.source = image_path
    #     predicted_class, predicted_score = predict(model, image_path)
    #     scoree = float(predicted_score) * 100
    #     self.ids.result_class.text = "Predicted Class: " + predicted_class
    #     self.ids.result_perc.text = "Predicted Score: " + str(scoree) + " %"
    pass
