import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
from tools import *


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.original_image = ''
        self.current_image = ''

        # Zone d'affichage de l'image
        self.image_label = tk.Label(self.root, text='image goes here')
        self.image_label.grid(row=0, column=1, rowspan=6)

        self.scale_frame = tk.Frame(self.root)
        self.scale_frame.grid(row=1, column=0, rowspan=4)

        # Curseurs pour ajuster la luminosité, le contraste et l'exposition
        self.brightness_scale = tk.Scale(self.scale_frame, label="Luminosité", from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL,
                                         command=self.update_brightness)
        self.brightness_scale.set(1.0)
        self.brightness_scale.grid(row=0, column=0)

        self.contrast_scale = tk.Scale(self.scale_frame, label="Contraste", from_=-255, to=255, resolution=1, orient=tk.HORIZONTAL,
                                       command=self.update_contrast)
        self.contrast_scale.set(1.0)
        self.contrast_scale.grid(row=1, column=0)

        self.exposure_scale = tk.Scale(self.scale_frame, label="Exposition", from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL,
                                       command=self.update_exposure)
        self.exposure_scale.set(1.0)
        self.exposure_scale.grid(row=2, column=0)

        self.binary_threshold_scale = tk.Scale(self.scale_frame, label="Set threshold", from_=0, to=255, resolution=1,
                                               orient=tk.HORIZONTAL)
        self.binary_threshold_scale.set(50)
        self.binary_threshold_scale.grid(row=3, column=0)

        self.steps = [{'text': 'load Image', 'command': self.open_image, 'image': ''},
                      {'text': 'find moon', 'command': self.find_moon_handler, 'image': ''},
                      {'text': 'crop to moon', 'command': self.crop_handler, 'image': ''},
                      {'text': 'binarize', 'command': self.find_moon_handler, 'image': ''},
                      {'text': 'straighten', 'command': self.straighten_handler, 'image': ''},
                      {'text': 'compare', 'command': self.compare_handler, 'image': ''}]

        self.stepIndex = 0

        self.steps_frame = tk.Frame(self.root)
        self.steps_frame.grid(row=0, column=0)

        self.step_button = tk.Button(self.steps_frame, text=self.steps[0]['text'], command=self.steps[0]['command'])
        self.step_button.grid(row=0, column=0, columnspan=2, pady=5)

        self.step_minus = tk.Button(self.steps_frame, text='back', bg='gray', command=self.previous_step_handler)
        self.step_minus.grid(row=1, column=0, padx=5)

        self.step_plus = tk.Button(self.steps_frame, text='next', command=self.next_step_handler)
        self.step_plus.grid(row=1, column=1)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)

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
            self.step_button.config(text=self.steps[self.stepIndex]['text'], command=self.steps[self.stepIndex]['command'])
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
            self.step_button.config(text=self.steps[self.stepIndex]['text'], command=self.steps[self.stepIndex]['command'])
            if self.steps[self.stepIndex]['image']:
                print(f'setting image to {self.stepIndex}')
                self.update_display(self.steps[self.stepIndex]['image'])

    def compare_handler(self):
        img = np.array(self.current_image)
        phase_img, sim_name, sim_index = get_most_similar(img, 'Images/phases',
                                                          thresh=self.binary_threshold_scale.get())
        self.image_label = Result(self.root, self.original_image, self.current_image, Image.fromarray(phase_img),
                                  sim_name)
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
        self.current_image = Image.fromarray(straighten(img))
        self.update_display(self.current_image)

    def open_image(self):
        # Ouvrir l'explorateur de fichiers
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if file_path:
            # Charger l'image sélectionnée
            self.original_image = Image.open(file_path)
            self.current_image = self.original_image
            self.update_display(self.original_image)

            # Mettre à jour les curseurs
            self.brightness_scale.set(1.0)
            self.contrast_scale.set(1.0)
            self.exposure_scale.set(1.0)

    def update_brightness(self, *args):
        pass

    def update_contrast(self, *args):
        if self.current_image:
            level = self.contrast_scale.get()
            factor = (259 * (level + 255)) / (255 * (259 - level))
            print(factor)

            def contrast(c):
                value = 128 + factor * (c - 128)
                return max(0, min(255, value))

            self.current_image.point(contrast)
            self.update_display(self.current_image)

    def update_exposure(self, *args):
        pass

    def update_display(self, new_image):
        self.steps[self.stepIndex]['image'] = new_image
        to_display = new_image.copy()
        to_display.thumbnail((500, 500))
        # Convertir l'image pour Tkinter
        self.tk_image = ImageTk.PhotoImage(to_display)

        # Mettre à jour l'étiquette avec la nouvelle image
        self.image_label.config(image=self.tk_image)


class Result(tk.Frame):
    def __init__(self, parent, original_image, cropped_image, phase_image, phase_name):
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
        self.phase_name_label.grid(row=2, column=0, columnspan=2)


# Créer une instance de la classe ImageViewer
root = tk.Tk()
# app = Result(root, Image.open('Images/Paysages/Ciel03.jpg'),
#              Image.open('Images/Paysages/Ciel03-edit.jpg'),
#              Image.open('Images/phases/7.png'),
#              '7.png')

app = ImageViewer(root)

# Définir la taille minimale de la fenêtre à 800x800 pixels
root.minsize(800, 800)

# Lancer la boucle principale de l'interface
root.mainloop()
