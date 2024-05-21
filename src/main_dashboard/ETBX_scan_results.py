from kivy.uix.screenmanager import Screen   
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton   

from components.classifier_only import load_model_from_file, predict

# Load the trained model
model = load_model_from_file('assets\ml-model\efficientNetB7_v0-5.h5')

Builder.load_file("main_dashboard/maindash_kivy_files/etbx_scan_res.kv")



class ScanResult(Screen):
    def update_result(self, image_path):
        global xrayRes
        xrayRes = image_path
        self.ids.res_img.source = xrayRes
        predicted_class, predicted_score = predict(model, image_path)
        if predicted_class == "tuberculosis":
            predicted_class = "TB Positive: "
        else:
            predicted_class = "Non-TB: "    
        scoree = round(float(predicted_score) * 100, 2)
        #self.ids.percent_bar.size = self.parent.width * 0.35 * predicted_score, self.parent.height * 0.03
        self.ids.result_classnPerc.text = predicted_class + str(scoree) + " %"

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