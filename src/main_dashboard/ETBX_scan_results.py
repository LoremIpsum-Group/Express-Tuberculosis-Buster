from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder

from components.classifier_only import load_model_from_file, predict

# Load the trained model
model = load_model_from_file('assets\ml-model\efficientnetB3_V0_6_1.h5')

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_res.kv")

class ScanResult(Screen):
    def update_result(self, image_path):
        self.ids.res_img.source = image_path
        predicted_class, predicted_score = predict(model, image_path)
        if predicted_class == "tuberculosis":
            predicted_class = "TB Positive: "
        else:
            predicted_class = "Non-TB: "    
        scoree = round(float(predicted_score) * 100, 2)
        #self.ids.percent_bar.size = (self.parent.width * 0.35 * predicted_score, self.parent.height * 0.03)
        self.ids.result_classnPerc.text = predicted_class + str(scoree) + " %"

    pass
