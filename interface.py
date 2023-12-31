import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter.constants import *
from PIL import Image, ImageTk, ImageEnhance
from tools import *


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.original_image = ''
        self.current_image = ''

        self.steps_frame = tk.Frame(self.root)
        self.steps_frame.grid(row=0, column=0)

        self.scale_frame = tk.Frame(self.root)
        self.scale_frame.grid(row=1, column=0, rowspan=1)

        self.image_label = tk.Label(self.root, text='image goes here')
        self.image_label.grid(row=0, column=1, rowspan=2)

        # Curseurs pour ajuster la luminosité, le contraste et l'exposition
        self.brightness_scale = tk.Scale(self.scale_frame, label="Luminosité", from_=0, to=2, resolution=0.1,
                                         orient=tk.HORIZONTAL,
                                         command=self.update_image)
        self.brightness_scale.set(1.0)
        self.brightness_scale.grid(row=0, column=0)

        self.contrast_scale = tk.Scale(self.scale_frame, label="Contraste", from_=0, to=2, resolution=0.1,
                                       orient=tk.HORIZONTAL,
                                       command=self.update_image)
        self.contrast_scale.set(1.0)
        self.contrast_scale.grid(row=1, column=0)

        self.color_scale = tk.Scale(self.scale_frame, label="Couleur", from_=0, to=2, resolution=0.1,
                                       orient=tk.HORIZONTAL,
                                       command=self.update_image)
        self.color_scale.set(1.0)
        self.color_scale.grid(row=2, column=0)

        self.binary_threshold_scale = tk.Scale(self.scale_frame, label="Set threshold", from_=0, to=255, resolution=1,
                                               orient=tk.HORIZONTAL)
        self.binary_threshold_scale.set(50)
        self.binary_threshold_scale.grid(row=3, column=0)

        self.steps = [{'text': 'load Image', 'command': self.open_image, 'image': ''},
                      {'text': 'find moon', 'command': self.find_moon_handler, 'image': ''},
                      {'text': 'crop to moon', 'command': self.crop_handler, 'image': ''},
                      {'text': 'binarize', 'command': self.binarize_handler, 'image': ''},
                      {'text': 'straighten', 'command': self.straighten_handler, 'image': ''},
                      {'text': 'compare', 'command': self.compare_handler, 'image': ''}]

        self.stepIndex = 0

        self.step_button = tk.Button(self.steps_frame, text=self.steps[0]['text'], command=self.steps[0]['command'])
        self.step_button.grid(row=0, column=0, columnspan=2, pady=5)

        self.step_minus = tk.Button(self.steps_frame, text='back', bg='gray', command=self.previous_step_handler)
        self.step_minus.grid(row=1, column=0, padx=5)

        self.step_plus = tk.Button(self.steps_frame, text='next', command=self.next_step_handler)
        self.step_plus.grid(row=1, column=1)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)
        root.columnconfigure(2, weight=1)

    def next_step_handler(self):
        num_steps = len(self.steps)

        if self.stepIndex == (num_steps - 1):
            return
        else:
            if self.stepIndex == 0:
                self.step_minus.config(bg='SystemButtonFace')
            self.stepIndex += 1
            if self.stepIndex == (num_steps - 1):
                self.step_plus.config(bg='gray')
            self.step_button.config(text=self.steps[self.stepIndex]['text'],
                                    command=self.steps[self.stepIndex]['command'])
            if self.steps[self.stepIndex]['image']:
                print(f'setting image to {self.stepIndex}')
                self.update_display(self.steps[self.stepIndex]['image'])

    def previous_step_handler(self):
        num_steps = len(self.steps)

        if self.stepIndex == 0:
            return
        else:
            if self.stepIndex == (num_steps - 1):
                self.step_plus.config(bg='SystemButtonFace')
                self.image_label.destroy()
                self.image_label = tk.Label(self.root, text='image goes here')
                self.image_label.grid(row=0, column=1, rowspan=6)
            self.stepIndex -= 1
            if self.stepIndex == 0:
                self.step_minus.config(bg='gray')
            self.step_button.config(text=self.steps[self.stepIndex]['text'],
                                    command=self.steps[self.stepIndex]['command'])
            if self.steps[self.stepIndex]['image']:
                print(f'setting image to {self.stepIndex}')
                self.update_display(self.steps[self.stepIndex]['image'])

    def compare_handler(self):
        img = np.array(self.current_image)
        phase_img, sim_name, sim_index = get_most_similar(img, 'Images/phases',
                                                          thresh=self.binary_threshold_scale.get())
        self.image_label = Result(self.root, self.original_image, self.current_image, Image.fromarray(phase_img),
                                  sim_name, sim_index)
        self.image_label.grid(row=0, column=1, rowspan=6)

    def find_moon_handler(self):
        img = np.array(self.current_image)
        moon_coords = moon_coordinates(img)
        with_circle = circle_display_on_image(img, moon_coords)
        self.update_display(Image.fromarray(with_circle))

    def crop_handler(self):
        img = np.array(self.current_image)
        moon_coords = moon_coordinates(img)
        cropped = crop_to_circle(img, moon_coords[0], moon_coords[1], moon_coords[2])
        self.current_image = Image.fromarray(cropped)
        self.update_display(self.current_image)

    def straighten_handler(self):
        img = np.array(self.current_image)
        self.current_image = Image.fromarray(straighten(img, self.binary_threshold_scale.get()))
        self.update_display(self.current_image)

    def open_image(self):
        # Ouvrir l'explorateur de fichiers
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if file_path:
            # Charger l'image sélectionnée
            self.original_image = Image.open(file_path)
            self.current_image = self.original_image

            # Reinitialiser l'historique d'image
            for step in self.steps:
                step['image'] = ''

            # Afficher l'image
            self.update_display(self.original_image)

            # Mettre à jour les curseurs
            self.brightness_scale.set(1.0)
            self.contrast_scale.set(1.0)
            self.color_scale.set(1.0)

    def binarize_handler(self):
        img = np.array(self.current_image)
        binarized = binarize_image(img, thresh_value=self.binary_threshold_scale.get())
        self.update_display(Image.fromarray(binarized))

    def update_image(self, *args):
        if not isinstance(self.original_image, Image.Image):
            return
        brightness_value = self.brightness_scale.get()
        contrast_value = self.contrast_scale.get()
        color_value = self.color_scale.get()

        if brightness_value == 0:
            brightness_value = 0.01
        if contrast_value == 0:
            contrast_value = 0.01
        if color_value == 0:
            color_value = 0.01

        self.current_image = self.original_image.copy()

        enhancer = ImageEnhance.Brightness(self.current_image)
        self.current_image = enhancer.enhance(brightness_value)

        enhancer = ImageEnhance.Contrast(self.current_image)
        self.current_image = enhancer.enhance(contrast_value)

        enhancer = ImageEnhance.Color(self.current_image)
        self.current_image = enhancer.enhance(color_value)

        self.update_display(self.current_image)

    def update_display(self, new_image):
        self.steps[self.stepIndex]['image'] = new_image
        to_display = new_image.copy()
        to_display.thumbnail((500, 500))

        self.tk_image = ImageTk.PhotoImage(to_display)
        self.image_label.config(image=self.tk_image)


class Result(tk.Frame):
    def __init__(self, parent, original_image, cropped_image, phase_image, phase_name, index):
        tk.Frame.__init__(self, parent)

        original_image.thumbnail((500, 500))
        self.original_image = ImageTk.PhotoImage(original_image)
        self.original_image_label = tk.Label(self, image=self.original_image)
        self.original_image_label.grid(row=0, column=0, columnspan=2)

        cropped_image.thumbnail((250, 250))
        self.cropped_image = ImageTk.PhotoImage(cropped_image)
        self.cropped_image_label = tk.Label(self, image=self.cropped_image)
        self.cropped_image_label.grid(row=1, column=0, columnspan=1)

        phase_image.thumbnail((250, 250))
        self.phase_image = ImageTk.PhotoImage(phase_image)
        self.phase_image_label = tk.Label(self, image=self.phase_image)
        self.phase_image_label.grid(row=1, column=1, columnspan=1)

        self.phase_name_label = tk.Label(self, text=phase_name)
        self.phase_name_label.grid(row=2, column=0, columnspan=1)

        self.index_label = tk.Label(self, text=f"SSI : {index}")
        self.index_label.grid(row=2, column=1, columnspan=1)


# Créer une instance de la classe ImageViewer
root = tk.Tk()
app = ImageViewer(root)

# Définir la taille minimale de la fenêtre à 800x800 pixels
root.minsize(800, 800)

# Lancer la boucle principale de l'interface
root.mainloop()
