import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.open_button = tk.Button(root, text="Ouvrir une image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.brightness_scale = tk.Scale(root, label="Luminosité", from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_scale.set(1.0)
        self.brightness_scale.pack(pady=5)

        self.contrast_scale = tk.Scale(root, label="Contraste", from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_scale.set(1.0)
        self.contrast_scale.pack(pady=5)

        self.exposure_scale = tk.Scale(root, label="Exposition", from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_exposure)
        self.exposure_scale.set(1.0)
        self.exposure_scale.pack(pady=5)

        self.current_brightness = 1.0
        self.current_contrast = 1.0
        self.current_exposure = 1.0

        # Stocker les dernières valeurs des curseurs
        self.last_brightness_value = 1.0
        self.last_contrast_value = 1.0
        self.last_exposure_value = 1.0

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if file_path:
            self.original_image = Image.open(file_path)
            self.original_image.thumbnail((500, 500))
            self.tk_image = ImageTk.PhotoImage(self.original_image)
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image

            self.brightness_scale.set(self.current_brightness)
            self.contrast_scale.set(self.current_contrast)
            self.exposure_scale.set(self.current_exposure)

    def update_brightness(self, *args):
        brightness_value = self.brightness_scale.get()

        # Vérifier si tous les curseurs sont à leur valeur minimale
        if brightness_value == 1.0 and self.contrast_scale.get() == 1.0 and self.exposure_scale.get() == 1.0:
            enhanced_image = self.original_image
        else:
            # Mettre à jour les valeurs actuelles des curseurs
            self.current_brightness = self.last_brightness_value * brightness_value
            self.current_contrast = self.current_contrast / self.last_brightness_value * brightness_value
            self.current_exposure = self.current_exposure / self.last_brightness_value * brightness_value

            # Stocker la dernière valeur réelle du curseur
            self.last_brightness_value = brightness_value

            enhanced_image = self.apply_adjustments()

        self.update_display(enhanced_image)

    def update_contrast(self, *args):
        contrast_value = self.contrast_scale.get()

        # Vérifier si tous les curseurs sont à leur valeur minimale
        if self.brightness_scale.get() == 1.0 and contrast_value == 1.0 and self.exposure_scale.get() == 1.0:
            enhanced_image = self.original_image
        else:
            # Mettre à jour les valeurs actuelles des curseurs
            self.current_brightness = self.current_brightness / self.last_contrast_value * contrast_value
            self.current_contrast = self.last_contrast_value * contrast_value
            self.current_exposure = self.current_exposure / self.last_contrast_value * contrast_value

            # Stocker la dernière valeur réelle du curseur
            self.last_contrast_value = contrast_value

            enhanced_image = self.apply_adjustments()

        self.update_display(enhanced_image)

    def update_exposure(self, *args):
        exposure_value = self.exposure_scale.get()

        # Vérifier si tous les curseurs sont à leur valeur minimale
        if self.brightness_scale.get() == 1.0 and self.contrast_scale.get() == 1.0 and exposure_value == 1.0:
            enhanced_image = self.original_image
        else:
            # Mettre à jour les valeurs actuelles des curseurs
            self.current_brightness = self.current_brightness / self.last_exposure_value * exposure_value
            self.current_contrast = self.current_contrast / self.last_exposure_value * exposure_value
            self.current_exposure = self.last_exposure_value * exposure_value

            # Stocker la dernière valeur réelle du curseur
            self.last_exposure_value = exposure_value

            enhanced_image = self.apply_adjustments()

        self.update_display(enhanced_image)

    def apply_adjustments(self):
        brightness_value = self.current_brightness
        contrast_value = self.current_contrast
        exposure_value = self.current_exposure

        enhanced_image = ImageEnhance.Brightness(self.original_image).enhance(brightness_value)
        enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast_value)
        enhanced_image = ImageEnhance.Color(enhanced_image).enhance(exposure_value)

        return enhanced_image

    def update_display(self, enhanced_image):
        tk_image = ImageTk.PhotoImage(enhanced_image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image


# Créer une instance de la classe ImageViewer
root = tk.Tk()
app = ImageViewer(root)

# Définir la taille minimale de la fenêtre à 800x800 pixels
root.minsize(800, 800)

# Lancer la boucle principale de l'interface
root.mainloop()