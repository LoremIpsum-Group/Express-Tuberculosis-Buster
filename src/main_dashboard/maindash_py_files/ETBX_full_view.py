import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class FullScreenApp:
    def __init__(self, root, image1_path, gradCamIm): 
        """
        Initializes the X-Ray Inspector class and defines the widgets present in the tkinter application.

        Parameters:
        - root: The root Tkinter window.
        - image1_path: a float32 x-ray image which will then be converted to uint8 to be displayed using the
        fromarray() function of the PIL library.
        - gradCamIm: a float32 gradcam layered image which will then be converted to uint8 to be displayed using the
        fromarray() function of the PIL library.

        Returns:
        None
        """
        self.root = root
        self.root.title("X-Ray Inspector")

        min_val1 = np.min(image1_path)
        max_val1 = np.max(image1_path)
        self.image1_data = ((image1_path - min_val1) / (max_val1 - min_val1) * 255).astype(np.uint8)

        min_val = np.min(gradCamIm)
        max_val = np.max(gradCamIm)
        self.image2_data = ((gradCamIm - min_val) / (max_val - min_val) * 255).astype(np.uint8)

        self.root.configure(bg='black')

        self.root.attributes("-fullscreen", True)
        self.root.bind_all("<Escape>", lambda event: self.exit_fullscreen(event))
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.image1 = Image.fromarray(self.image1_data)
        self.image2 = Image.fromarray(self.image2_data)
        
        # self.image1 = Image.open(image1_path)
        # self.image2 = Image.open(image2_path)
        #self.small_image = Image.open("model_functions/sample_images/gradientImage.png")
        
        self.photo1 = self.resize_image(self.image1, self.screen_width // 2, self.screen_height )
        self.photo2 = self.resize_image(self.image2, self.screen_width // 2, self.screen_height )
            
        self.canvas1 = tk.Canvas(self.root, width=self.screen_width // 2, height=(self.screen_height - int(self.screen_height*.1)), bg='black', highlightthickness=0, borderwidth=0)
        self.canvas2 = tk.Canvas(self.root, width=self.screen_width // 2, height=(self.screen_height - int(self.screen_height*.1)), bg='black', highlightthickness=0, borderwidth=0)
        
        self.image_id1 = self.canvas1.create_image(0, 0, anchor="nw", image=self.photo1)
        self.image_id2 = self.canvas2.create_image(0, 0, anchor="nw", image=self.photo2)

        self.canvas1.grid(row = 0, column= 0, sticky = "n")
        self.canvas2.grid(row = 0, column= 1, sticky = "n")
        
        self.bottom_frame = tk.Frame(self.root, highlightthickness=0, borderwidth=0)
        self.bottom_frame.grid(row=1, column=0, columnspan = 2, sticky="s")

        # Load an image
        self.image = Image.open("assets/gradientImage2.png")
        self.photo = ImageTk.PhotoImage(self.image)

        # Add image to a label
        self.image_label = tk.Label(self.bottom_frame, image=self.photo)
        self.image_label.pack(side="right")

        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.exit_fullscreen, bg='red', fg='white', font=("Helvetica", 12))
        self.exit_button.pack(side="left", pady=10, padx=10)

        self.instruction_label = tk.Label(self.bottom_frame, text="ScrollUp: Zoom In     ScrollDown: Zoom Out", fg="white", bg='black', font=("Helvetica", 12))
        self.instruction_label.pack(side="left")

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
        """
        Resize the given image while maintaining the aspect ratio.

        Args:
            image (PIL.Image.Image): The image to be resized.
            target_width (int): The desired width of the resized image.
            max_height (int): The maximum height of the resized image.

        Returns:
            PIL.ImageTk.PhotoImage: The resized image as a PhotoImage object.
        """
        width_percent = target_width / float(image.size[0])
        new_height = int((float(image.size[1]) * float(width_percent)))

        if new_height > max_height:
            height_percent = max_height / float(image.size[1])
            new_width = int((float(image.size[0]) * float(height_percent)))
            return ImageTk.PhotoImage(image.resize((new_width, max_height), Image.LANCZOS))

        return ImageTk.PhotoImage(image.resize((target_width, new_height), Image.LANCZOS))

    def on_button_press(self, event):
        """
        Callback function for button press event.

        Parameters:
            event (Event): The event object containing information about the button press.

        Returns:
            None
        """
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        """
        Handles the dragging of images on the canvas. This function also creates a shape around the image
        which will help in containing it inside of the defined canvas. 

        Args:
            event (Event): The event object containing information about the drag event.

        Returns:
            None
        """
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.canvas1.move(self.image_id1, dx, dy)
        self.canvas2.move(self.image_id2, dx, dy)

        self.start_x = event.x
        self.start_y = event.y

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

    def on_zoom(self, event):
        """
        Handles the zoom functionality when the user scrolls the mouse wheel.

        Args:
            event (tk.Event): The event object containing information about the event.

        Returns:
            None
        """

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

        for canvas, image_id in [(self.canvas1, self.image_id1), (self.canvas2, self.image_id2)]:
            bbox = canvas.bbox(image_id)
            new_x = event.x - (event.x - bbox[0]) * scale_factor
            new_y = event.y - (event.y - bbox[1]) * scale_factor
            canvas.coords(image_id, new_x, new_y)

            x0, y0, x1, y1 = canvas.bbox(image_id)
            if x0 > 0:
                canvas.move(image_id, -x0, 0)
            if y0 > 0:
                canvas.move(image_id, 0, -y0)
            if x1 < canvas.winfo_width():
                canvas.move(image_id, canvas.winfo_width() - x1, 0)
            if y1 < canvas.winfo_height():
                canvas.move(image_id, 0, canvas.winfo_height() - y1)

        self.canvas1.config(scrollregion=self.canvas1.bbox(tk.ALL))
        self.canvas2.config(scrollregion=self.canvas2.bbox(tk.ALL))

    def exit_fullscreen(self, event=None):
        self.root.destroy()

def xray_full_app(imgPath1, gradCam):
    root = tk.Tk()
    app = FullScreenApp(root, imgPath1, gradCam)
    root.mainloop()