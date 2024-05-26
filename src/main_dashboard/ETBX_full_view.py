import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class FullScreenApp:
    def __init__(self, root, image1_path, gradCamIm):
        self.root = root
        self.root.title("X-Ray Inspector")

        min_val = np.min(gradCamIm)
        max_val = np.max(gradCamIm)
        self.image2_data = ((gradCamIm - min_val) / (max_val - min_val) * 255).astype(np.uint8)

        self.root.configure(bg='black')

        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.image1 = Image.open(image1_path)
        self.image2 = Image.fromarray(self.image2_data)
        
        self.photo1 = self.resize_image(self.image1, self.screen_width // 2, self.screen_height)
        self.photo2 = self.resize_image(self.image2, self.screen_width // 2, self.screen_height)
        
        self.canvas1 = tk.Canvas(self.root, width=self.screen_width // 2, height=self.screen_height, bg='black', highlightthickness=0, borderwidth=0)
        self.canvas2 = tk.Canvas(self.root, width=self.screen_width // 2, height=self.screen_height, bg='black', highlightthickness=0, borderwidth=0)
        
        self.image_id1 = self.canvas1.create_image(0, 0, anchor="nw", image=self.photo1)
        self.image_id2 = self.canvas2.create_image(0, 0, anchor="nw", image=self.photo2)
        
        self.canvas1.pack(side="left", expand=True, fill="both")
        self.canvas2.pack(side="right", expand=True, fill="both")
        
        self.canvas1.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas1.bind("<B1-Motion>", self.on_drag)
        self.canvas1.bind("<MouseWheel>", self.on_zoom)
        
        self.canvas2.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas2.bind("<B1-Motion>", self.on_drag)
        self.canvas2.bind("<MouseWheel>", self.on_zoom)
        
        self.current_image1 = self.image1
        self.current_image2 = self.image2
        self.scale_factor1 = 1.0
        self.scale_factor2 = 1.0

    def resize_image(self, image, target_width, max_height):
        width_percent = target_width / float(image.size[0])
        new_height = int((float(image.size[1]) * float(width_percent)))
        
        if new_height > max_height:
            height_percent = max_height / float(image.size[1])
            new_width = int((float(image.size[0]) * float(height_percent)))
            return ImageTk.PhotoImage(image.resize((new_width, max_height), Image.LANCZOS))
        
        return ImageTk.PhotoImage(image.resize((target_width, new_height), Image.LANCZOS))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        bbox1 = self.canvas1.bbox(self.image_id1)
        bbox2 = self.canvas2.bbox(self.image_id2)

        new_x0_1 = bbox1[0] + dx
        new_y0_1 = bbox1[1] + dy
        new_x1_1 = bbox1[2] + dx
        new_y1_1 = bbox1[3] + dy

        new_x0_2 = bbox2[0] + dx
        new_y0_2 = bbox2[1] + dy
        new_x1_2 = bbox2[2] + dx
        new_y1_2 = bbox2[3] + dy

        if new_x0_1 > 0:
            dx = -bbox1[0]
        if new_y0_1 > 0:
            dy = -bbox1[1]
        if new_x1_1 < self.canvas1.winfo_width():
            dx = self.canvas1.winfo_width() - bbox1[2]
        if new_y1_1 < self.canvas1.winfo_height():
            dy = self.canvas1.winfo_height() - bbox1[3]

        if new_x0_2 > 0:
            dx = -bbox2[0]
        if new_y0_2 > 0:
            dy = -bbox2[1]
        if new_x1_2 < self.canvas2.winfo_width():
            dx = self.canvas2.winfo_width() - bbox2[2]
        if new_y1_2 < self.canvas2.winfo_height():
            dy = self.canvas2.winfo_height() - bbox2[3]

        self.canvas1.move(self.image_id1, dx, dy)
        self.canvas2.move(self.image_id2, dx, dy)
        
        self.start_x = event.x
        self.start_y = event.y

    def on_zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9

        self.scale_factor1 *= scale_factor
        self.scale_factor2 *= scale_factor

        new_image1 = self.image1.resize(
            (int(self.image1.width * self.scale_factor1), int(self.image1.height * self.scale_factor1)),
            Image.LANCZOS
        )
        self.photo1 = ImageTk.PhotoImage(new_image1)
        self.canvas1.itemconfig(self.image_id1, image=self.photo1)
        
        new_image2 = self.image2.resize(
            (int(self.image2.width * self.scale_factor2), int(self.image2.height * self.scale_factor2)),
            Image.LANCZOS
        )
        self.photo2 = ImageTk.PhotoImage(new_image2)
        self.canvas2.itemconfig(self.image_id2, image=self.photo2)

        bbox1 = self.canvas1.bbox(self.image_id1)
        bbox2 = self.canvas2.bbox(self.image_id2)
        new_x1 = event.x - (event.x - bbox1[0]) * scale_factor
        new_y1 = event.y - (event.y - bbox1[1]) * scale_factor
        new_x2 = event.x - (event.x - bbox2[0]) * scale_factor
        new_y2 = event.y - (event.y - bbox2[1]) * scale_factor

        self.canvas1.coords(self.image_id1, new_x1, new_y1)
        self.canvas2.coords(self.image_id2, new_x2, new_y2)

        x0, y0, x1, y1 = self.canvas1.bbox(self.image_id1)
        if x0 > 0:
            self.canvas1.move(self.image_id1, -x0, 0)
        if y0 > 0:
            self.canvas1.move(self.image_id1, 0, -y0)
        if x1 < self.canvas1.winfo_width():
            self.canvas1.move(self.image_id1, self.canvas1.winfo_width() - x1, 0)
        if y1 < self.canvas1.winfo_height():
            self.canvas1.move(self.image_id1, 0, self.canvas1.winfo_height() - y1)

        x0, y0, x1, y1 = self.canvas2.bbox(self.image_id2)
        if x0 > 0:
            self.canvas2.move(self.image_id2, -x0, 0)
        if y0 > 0:
            self.canvas2.move(self.image_id2, 0, -y0)
        if x1 < self.canvas2.winfo_width():
            self.canvas2.move(self.image_id2, self.canvas2.winfo_width() - x1, 0)
        if y1 < self.canvas2.winfo_height():
            self.canvas2.move(self.image_id2, 0, self.canvas2.winfo_height() - y1)

        self.canvas1.config(scrollregion=self.canvas1.bbox(tk.ALL))
        self.canvas2.config(scrollregion=self.canvas2.bbox(tk.ALL))

    def exit_fullscreen(self, event=None):
        self.root.destroy()
        # self.root.attributes("-fullscreen", False)
        # self.root.quit()

def xray_full_app(imgPath1, gradCam):
    root = tk.Tk()
    app = FullScreenApp(root, imgPath1, gradCam)
    root.mainloop()