from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from PIL import Image
import io
import base64
import os
import numpy as np
import sqlite3


class ScanResultData:
    def __init__(self):
        self.results = None
        self.percentage = None
        self.orig_img = None
        self.preproc_img = None
        self.gradcam_img = None
        self.notes = None
        self.is_misclassified = None


scan_result = ScanResultData()

Builder.load_file("etbx_scan_res.kv")


class ScanResult(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_classifier = None
        self.model_segmentation = None

        # conn = sqlite3.connect("assets/view_record_main.db")
        # c = conn.cursor()
        # c.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS RESULTS (
        #         result_id INTEGER PRIMARY KEY,
        #         patient_id INTEGER,
        #         date_of_scan TEXT NOT NULL,
        #         result TEXT NOT NULL,
        #         percentage REAL,
        #         orig_image BLOB NOT NULL,
        #         preproc_image BLOB NOT NULL,
        #         grad_cam_image BLOB NOT NULL,
        #         notes TEXT,
        #         misclassified BOOLEAN,
        #         FOREIGN KEY(patient_id) REFERENCES PATIENT(patient_id)
        #     )
        # """
        # )
        # conn.commit()
        # conn.close()

    def img_string(self, image):
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            contents = output.getvalue()
        img_data = base64.b64encode(contents).decode("ascii")
        return "data:image/png;base64," + img_data

    def update_result(self, image_path="assets/jpg.png", is_dicom=False):
        global xray_orig, xray_orig_resized, superimposed_img, masked_image

        xray_orig = image_path

        self.ids.res_img.source = xray_orig
        self.ids.x_ray.md_bg_color = (0.1, 0.5, 0.9, 1)
        self.ids.x_ray.text_color = (1, 1, 1, 1)

        # Core functionalities
        cropped_img = Image.open(xray_orig).resize((512, 512))
        xray_orig_resized = cropped_img
        masked_image = np.array(cropped_img)  # Dummy segmentation
        segment_bad = (False, "All good")

        if not segment_bad[0]:
            self.show_warning_popup(segment_bad[1])
        else:
            self.show_warning_popup(segment_bad[1])

        predicted_class = "Tuberculosis"
        predicted_score = 50  # Arbitrary score
        superimposed_img = cropped_img  # Dummy GradCAM

        bar_color = None
        sys_suggest = None
        x1 = None
        x2 = None
        if (predicted_score <= 25):
            bar_color = (0, 1, 0, 1)
            sys_suggest = "System does not see manifestations"
            x1 = .67
            x2 = .68
        elif (predicted_score <= 49):
            bar_color = (1, 1, 0, 1)
            sys_suggest = "Suggested for further screening."
            x1 = .67
            x2 = .67
        elif (predicted_score <= 74):
            bar_color = (1, 0.5, 0, 1)
            sys_suggest = "Visible signs, further screening highly suggested"
            x1 = .65
            x2 = .72
        else:
            bar_color = (1, 0, 0, 1)
            sys_suggest = "TB signs evident, immediate attention suggested."
            x1 = .65
            x2 = .715

        self.percentage = int(predicted_score)
        self.percentage_color = bar_color
        self.ids.result_classnPerc.text = predicted_class + ": " +str(predicted_score)
        self.ids.result_classnPerc.pos_hint = {"center_x": x1, "center_y": 0.76}
        self.ids.result_rcmdtn.text = sys_suggest
        self.ids.result_rcmdtn.pos_hint = {"center_x": x2, "center_y": 0.70}
        scan_result.results = predicted_class
        scan_result.percentage = predicted_score
        scan_result.orig_img = xray_orig
        scan_result.preproc_img = masked_image
        scan_result.gradcam_img = superimposed_img
        scan_result.notes = self.ids.notes.text

    def change_img(self, instance):
        white = (1, 1, 1, 1)
        blue = (0.1, 0.5, 0.9, 1)

        self.ids.x_ray.md_bg_color = white
        self.ids.x_ray.text_color = blue
        self.ids.pre_proc.md_bg_color = white
        self.ids.pre_proc.text_color = blue
        self.ids.grad_cam.md_bg_color = white
        self.ids.grad_cam.text_color = blue

        instance.md_bg_color = blue
        instance.text_color = white

        if instance == self.ids.x_ray:
            image = Image.fromarray(np.array(xray_orig_resized))
            self.ids.res_img.source = self.img_string(image)
        elif instance == self.ids.grad_cam:
            img = superimposed_img
            self.ids.res_img.source = self.img_string(img)
        elif instance == self.ids.pre_proc:
            img = Image.fromarray(((1.0 - masked_image) * 255).astype(np.uint8))
            img = img.convert("L")
            self.ids.res_img.source = self.img_string(img)

    def full_view(self):
        xrayPath = xray_orig_resized
        supIM = superimposed_img
        xray_full_app(xrayPath, supIM)

    def back_button(self):
        content = BoxLayout(orientation="vertical")
        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)
        content.add_widget(
            Label(
                text="[b]Are you sure you want to go back?\nScan Results will be lost[/b]!",
                color=(0, 0, 1, 1),
                markup=True,
            )
        )

        inner_content = BoxLayout(
            orientation="horizontal", spacing=10, padding=10, size_hint_y=0.3
        )
        confirm_btn = Button(
            text="Confirm",
            background_color=(0, 0, 1, 1),
            background_normal="",
            on_press=self.confirm,
        )
        cancel_btn = Button(
            text="Cancel",
            background_color=(0, 0, 1, 1),
            background_normal="",
            on_press=self.close_popup,
        )
        inner_content.add_widget(confirm_btn)
        inner_content.add_widget(cancel_btn)
        content.add_widget(inner_content)

        self.popup = Popup(
            title="Confirm Action",
            content=content,
            size_hint=(0.4, 0.4),
            separator_color=(0, 0, 0, 0),
            background_color=(0, 0, 1, 0.5),
            auto_dismiss=False,
        )
        self.popup.open()

        # def confirm(self, instance):
        #     save_new_screen = self.manager.get_screen("save_new")
        #     save_existing_screen = self.manager.get_screen("save_existing")
        #     save_new_screen.ids.patient_id.text = ""
        #     save_new_screen.ids.first_name.text = ""
        #     save_new_screen.ids.last_name.text = ""
        #     save_new_screen.ids.birthdate.text = ""
        #     save_new_screen.ids.address.text = ""
        #     save_new_screen.ids.male.active = False
        #     save_new_screen.ids.female.active = False
        #     self.manager.get_screen("scan_result").ids.notes.text = ""
        #     self.ids.misclassified.active = False
        #     self.manager.get_screen("save_existing").ids.patient_id.text = ""
        #     self.manager.get_screen(
        #         "save_existing"
        #     ).ids.patient_search_result.clear_widgets()
        #     self.manager.get_screen("save_existing").ids.patient_search_result.add_widget(
        #         Label(
        #             text="[b]Search Patient ID to save[/b]",
        #             pos_hint={"center_x": 0.5, "center_y": 0.5},
        #             color=(0, 0, 0, 1),
        #             markup=True,
        #         )
        #     )
        white = (1, 1, 1, 1)
        blue = (0.1, 0.5, 0.9, 1)

        self.ids.x_ray.md_bg_color = white
        self.ids.x_ray.text_color = blue
        self.ids.pre_proc.md_bg_color = white
        self.ids.pre_proc.text_color = blue
        self.ids.grad_cam.md_bg_color = white
        self.ids.grad_cam.text_color = blue
        if os.path.isfile("assets/dicom_image.png"):
            os.remove("assets/dicom_image.png")
        self.manager.current = "scan_img"
        self.popup.dismiss()

    def close_popup(self, instance):
        self.popup.dismiss()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_warning_popup(self, message):
        content = BoxLayout(orientation="vertical")
        label = Label(text=message)
        close_button = Button(text="Close", on_press=self.close_popup)
        content.add_widget(label)
        content.add_widget(close_button)
        self.popup = Popup(
            title="", content=content, auto_dismiss=False, size_hint=(0.4, 0.4)
        )
        self.popup.open()
