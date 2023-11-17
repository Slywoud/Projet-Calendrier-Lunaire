import cv2
from skimage.metrics import structural_similarity as ssim
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os

def resize_images(img1, img2):
    # Charger les images
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)

    # Redimensionner les images pour qu'elles aient la même taille
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    return img1, img2

def compare_images(image1, image2):
    # Calculer le SSIM
    similarity_index, _ = ssim(image1, image2, full=True)

    return similarity_index

def find_best_match(reference_image, folder_path):
    # Charger et redimensionner l'image de référence
    ref_img = cv2.imread(reference_image)
    
    # Convertir l'image de référence en noir et blanc (niveaux de gris) et binariser
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    _, ref_binary = cv2.threshold(ref_gray, 50, 255, cv2.THRESH_BINARY)
    
    best_match = None
    max_compatibility = 0.0

    # Parcourir toutes les images du dossier
    for i in range(29):  # Images numérotées de 0 à 28
        image_path = os.path.join(folder_path, f"{i}.png")

        # Charger et redimensionner l'image du dossier
        folder_img, _ = resize_images(reference_image, image_path)

        # Convertir l'image du dossier en noir et blanc (niveaux de gris) et binariser
        folder_gray = cv2.cvtColor(folder_img, cv2.COLOR_BGR2GRAY)
        _, folder_binary = cv2.threshold(folder_gray, 50, 255, cv2.THRESH_BINARY)

        # Calculer le SSIM entre l'image de référence et l'image du dossier
        compatibility = compare_images(ref_binary, folder_binary)

        # Mettre à jour la meilleure correspondance si nécessaire
        if compatibility > max_compatibility:
            max_compatibility = compatibility
            best_match = image_path

    return best_match, max_compatibility

# Exemple d'utilisation
reference_image = "Images/phases/7.png"
folder_path = "Images/phases"

best_match, max_compatibility = find_best_match(reference_image, folder_path)

print(f"Meilleure correspondance : {best_match}")
print(f"Taux de compatibilité maximum : {max_compatibility}")

# Afficher les images binaires pour comparaison visuelle
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(cv2.imread(reference_image), cv2.COLOR_BGR2RGB))
plt.title('Image de référence')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(cv2.imread(best_match), cv2.COLOR_BGR2RGB))
plt.title('Meilleure correspondance')

plt.show()
