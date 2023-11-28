import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        # Créer un bouton pour ouvrir l'explorateur de fichiers
        self.open_button = tk.Button(root, text="Ouvrir une image", command=self.open_image)
        self.open_button.pack(pady=10)

        # Zone d'affichage de l'image
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Curseurs pour ajuster la luminosité, le contraste et l'exposition
        self.brightness_scale = tk.Scale(root, label="Luminosité", from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_scale.set(1.0)
        self.brightness_scale.pack(pady=5)

        self.contrast_scale = tk.Scale(root, label="Contraste", from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_scale.set(1.0)
        self.contrast_scale.pack(pady=5)

        self.exposure_scale = tk.Scale(root, label="Exposition", from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_exposure)
        self.exposure_scale.set(1.0)
        self.exposure_scale.pack(pady=5)

    def open_image(self):
        # Ouvrir l'explorateur de fichiers
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if file_path:
            # Charger l'image sélectionnée
            self.original_image = Image.open(file_path)

            # Redimensionner l'image sans déformer (maintient le ratio d'aspect)
            self.original_image.thumbnail((500, 500))  # Ajustez la taille maximale selon vos besoins

            # Convertir l'image en un format compatible avec Tkinter
            self.tk_image = ImageTk.PhotoImage(self.original_image)

            # Mettre à jour l'étiquette avec la nouvelle image
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image  # Gardez une référence à l'image pour éviter la collecte par le garbage collector

            # Mettre à jour les curseurs
            self.brightness_scale.set(1.0)
            self.contrast_scale.set(1.0)
            self.exposure_scale.set(1.0)

    def update_brightness(self, *args):
        # Obtenir la valeur de la jauge de luminosité
        brightness_value = self.brightness_scale.get()

        # Appliquer l'ajustement à l'image
        enhanced_image = ImageEnhance.Brightness(self.original_image).enhance(brightness_value)

        # Mettre à jour l'affichage
        self.update_display(enhanced_image)

    def update_contrast(self, *args):
        # Obtenir la valeur de la jauge de contraste
        contrast_value = self.contrast_scale.get()

        # Appliquer l'ajustement à l'image
        enhanced_image = ImageEnhance.Contrast(self.original_image).enhance(contrast_value)

        # Mettre à jour l'affichage
        self.update_display(enhanced_image)

    def update_exposure(self, *args):
        # Obtenir la valeur de la jauge d'exposition
        exposure_value = self.exposure_scale.get()

        # Appliquer l'ajustement à l'image
        enhanced_image = ImageEnhance.Color(self.original_image).enhance(exposure_value)

        # Mettre à jour l'affichage
        self.update_display(enhanced_image)

    def update_display(self, enhanced_image):
        # Convertir l'image pour Tkinter
        tk_image = ImageTk.PhotoImage(enhanced_image)

        # Mettre à jour l'étiquette avec la nouvelle image
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image  # Gardez une référence à l'image pour éviter la collecte par le garbage collector

# Créer une instance de la classe ImageViewer
root = tk.Tk()
app = ImageViewer(root)

# Définir la taille minimale de la fenêtre à 800x800 pixels
root.minsize(800, 800)

# Lancer la boucle principale de l'interface
root.mainloop()