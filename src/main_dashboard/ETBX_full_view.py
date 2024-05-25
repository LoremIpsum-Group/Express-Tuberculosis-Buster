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
        
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.image1 = Image.open(image1_path)
        self.image2 = Image.fromarray(self.image2_data)
        
        self.photo1 = self.resize_image(self.image1, self.screen_width // 2, self.screen_height)
        self.photo2 = self.resize_image(self.image2, self.screen_width // 2, self.screen_height)
        
        self.canvas1 = tk.Canvas(self.root, width=self.screen_width // 2, height=self.screen_height, bg='black')
        self.canvas2 = tk.Canvas(self.root, width=self.screen_width // 2, height=self.screen_height, bg='black')
        
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
        self.canvas = event.widget

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        if self.canvas == self.canvas1:
            image_id = self.image_id1
            current_image = self.current_image1
        else:
            image_id = self.image_id2
            current_image = self.current_image2

        x0, y0, x1, y1 = self.canvas.bbox(image_id)

        new_x0 = x0 + dx
        new_y0 = y0 + dy
        new_x1 = x1 + dx
        new_y1 = y1 + dy

        if current_image.width > self.canvas.winfo_width():
            if new_x0 > 0:
                dx = -x0
            if new_x1 < self.canvas.winfo_width():
                dx = self.canvas.winfo_width() - x1
        else:
            dx = 0

        if current_image.height > self.canvas.winfo_height():
            if new_y0 > 0:
                dy = -y0
            if new_y1 < self.canvas.winfo_height():
                dy = self.canvas.winfo_height() - y1
        else:
            dy = 0

        self.canvas.move(image_id, dx, dy)
        
        self.start_x = event.x
        self.start_y = event.y

    def on_zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        canvas = event.widget

        mouse_x, mouse_y = event.x, event.y

        if canvas == self.canvas1:
            self.scale_factor1 *= scale_factor
            self.current_image1 = self.image1.resize(
                (int(self.image1.width * self.scale_factor1), int(self.image1.height * self.scale_factor1)),
                Image.LANCZOS
            )
            self.photo1 = ImageTk.PhotoImage(self.current_image1)
            image_id = self.image_id1
        else:
            self.scale_factor2 *= scale_factor
            self.current_image2 = self.image2.resize(
                (int(self.image2.width * self.scale_factor2), int(self.image2.height * self.scale_factor2)),
                Image.LANCZOS
            )
            self.photo2 = ImageTk.PhotoImage(self.current_image2)
            image_id = self.image_id2

        canvas.itemconfig(image_id, image=self.photo1 if canvas == self.canvas1 else self.photo2)

        bbox = canvas.bbox(image_id)
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        new_x = mouse_x - (mouse_x - bbox[0]) * scale_factor
        new_y = mouse_y - (mouse_y - bbox[1]) * scale_factor

        canvas.coords(image_id, new_x, new_y)

        x0, y0, x1, y1 = canvas.bbox(image_id)
        if x0 > 0:
            canvas.move(image_id, -x0, 0)
        if y0 > 0:
            canvas.move(image_id, 0, -y0)
        if x1 < canvas_width:
            canvas.move(image_id, canvas_width - x1, 0)
        if y1 < canvas_height:
            canvas.move(image_id, 0, canvas_height - y1)

        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    
    def exit_fullscreen(self, event=None):
        self.root.destroy()

def xray_full_app(imgPath1, gradCam):

    root = tk.Tk()
    

    app = FullScreenApp(root, imgPath1, gradCam)
    

    root.mainloop()
