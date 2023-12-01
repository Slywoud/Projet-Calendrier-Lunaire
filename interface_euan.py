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

        # Créer un bouton pour ouvrir l'explorateur de fichiers
        self.open_button = tk.Button(root, text="Ouvrir une image", command=self.open_image)
        self.open_button.grid(row=0,column=0)

        # Zone d'affichage de l'image
        self.image_label = tk.Label(root,text='image goes here')
        self.image_label.grid(row=0,column=1, rowspan=6)

        # Curseurs pour ajuster la luminosité, le contraste et l'exposition
        self.brightness_scale = tk.Scale(root, label="Luminosité", from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_scale.set(1.0)
        self.brightness_scale.grid(row=1,column=0)

        self.contrast_scale = tk.Scale(root, label="Contraste", from_=-255, to=255, resolution=1, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_scale.set(1.0)
        self.contrast_scale.grid(row=2,column=0)

        self.exposure_scale = tk.Scale(root, label="Exposition", from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_exposure)
        self.exposure_scale.set(1.0)
        self.exposure_scale.grid(row=3,column=0)

        self.crop_button = tk.Button(self.root, text="crop to moon", command=self.crop_handler)
        self.crop_button.grid(row=4,column=0)

        self.find_moon_button = tk.Button(self.root, text="find moon", command=self.find_moon_handler)
        self.find_moon_button.grid(row=5, column=0)

        self.straighten_button = tk.Button(self.root, text="straighten image", command=self.straighten_handler)
        self.straighten_button.grid(row=6, column=0)

        self.compare_button = tk.Button(self.root, text="determine phase", command=self.compare_handler)
        self.compare_button.grid(row=7, column=0)

        self.binary_threshold_scale = tk.Scale(self.root, label="Set threshold", from_=0, to=255, resolution=1,
                                               orient=tk.HORIZONTAL)
        self.binary_threshold_scale.set(50)
        self.binary_threshold_scale.grid(row=8, column=0)

        self.result_label = tk.Label(self.root, text='Results : ...')
        self.result_label.grid(row=7, column=1)


        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)

    def compare_handler(self):
        img = np.array(self.current_image)
        phase_img, sim_name, sim_index = get_most_similar(img, 'Images/phases', thresh=self.binary_threshold_scale.get())
        self.result_label.config(text=sim_name)
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

            # # Convertir l'image en un format compatible avec Tkinter
            # self.tk_image = ImageTk.PhotoImage(self.original_image)
            #
            # # Mettre à jour l'étiquette avec la nouvelle image
            # self.image_label.config(image=self.tk_image)
            # self.image_label.image = self.tk_image  # Gardez une référence à l'image pour éviter la collecte par le garbage collector
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
        to_display = new_image.copy()
        to_display.thumbnail((500, 500))
        # Convertir l'image pour Tkinter
        self.tk_image = ImageTk.PhotoImage(to_display)

        # Mettre à jour l'étiquette avec la nouvelle image
        self.image_label.config(image=self.tk_image)

# Créer une instance de la classe ImageViewer
root = tk.Tk()
app = ImageViewer(root)

# Définir la taille minimale de la fenêtre à 800x800 pixels
root.minsize(800, 800)

# Lancer la boucle principale de l'interface
root.mainloop()