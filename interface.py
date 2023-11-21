import compare  # Importez votre fichier compare.py
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Sélectionner l'image 1")
    return file_path

def interface_function(folder_path):
    # Laissez l'utilisateur choisir l'image1
    image_path1 = select_image()

    most_compatible = ''
    max_compatibility = 0.0

    for i in range(29):  # Images numérotées de 0 à 28
        image_path = os.path.join(folder_path, f"{i}.png")

        compatibility, image1, image2 = compare.compare_images(image_path1, image_path)
        print(f"Taux de compatibilité image {i}: {compatibility}")
        if compatibility > max_compatibility:
            max_compatibility = compatibility
            most_compatible = image2
            most_compatible_name = f"Phase : {i}"

    return max_compatibility, most_compatible, most_compatible_name

# Exemple d'utilisation de la fonction
if __name__ == "__main__":
    folder_path = "Images/phases/"

    max_compatibility, most_compatible, most_compatible_name = interface_function(folder_path)

    # Afficher les images binaires pour comparaison visuelle
    plt.subplot(1, 2, 1)
    plt.imshow(most_compatible, cmap='gray')
    plt.title('Image la plus compatible')

    plt.subplot(1, 2, 2)
    plt.text(0.5, 0.5, f"Phase la plus compatible:\n{most_compatible_name}\nTaux de compatibilité: {max_compatibility:.2f}",
             horizontalalignment='center', verticalalignment='center', fontsize=12)
    plt.axis('off')

    plt.show()
