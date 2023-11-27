import tools
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

    return tools.get_most_similar(image_path1, folder_path)

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
