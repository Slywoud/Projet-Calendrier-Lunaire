import cv2
from skimage.metrics import structural_similarity as ssim
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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

# Exemple d'utilisation
image_path1 = "Images/paysages/Ciel03-edit.jpg"
image_path2 = "Images/phases/7.png"

# Charger et redimensionner les images
img1, img2 = resize_images(image_path1, image_path2)

# Convertir l'image 1 en noir et blanc (niveaux de gris) et binariser
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
_, img1_binary = cv2.threshold(img1_gray, 50, 255, cv2.THRESH_BINARY)

# Binariser l'image 2
_, img2_binary = cv2.threshold(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY)

# Calculer le SSIM
compatibility = compare_images(img1_binary, img2_binary)
print(f"Taux de compatibilité : {compatibility}")

# Afficher les images binaires pour comparaison visuelle
plt.subplot(1, 2, 1)
plt.imshow(img1_binary, cmap='gray')
plt.title('Image 1 (binaire)')

plt.subplot(1, 2, 2)
plt.imshow(img2_binary, cmap='gray')
plt.title('Image 2 (binaire)')

plt.show()
