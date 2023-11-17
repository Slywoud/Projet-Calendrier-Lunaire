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

def binarize_image(image):
    img1_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, img1_binary = cv2.threshold(img1_gray, 100, 255, cv2.THRESH_BINARY)
    return img1_binary

def compare_images(image1, image2):
    # Calculer le SSIM
    image1, image2 = resize_images(image1, image2)
    image1 = binarize_image(image1)
    image2 = binarize_image(image2)
    similarity_index, _ = ssim(image1, image2, full=True)
    return similarity_index, image1, image2



# Exemple d'utilisation
image_path1 = "Images/paysages/Ciel03-edit.jpg"
folder_path = "Images/phases/"

most_compatible = ''
max_compatibility = 0.0

for i in range(29):  # Images numérotées de 0 à 28
    image_path = os.path.join(folder_path, f"{i}.png")

    compatibility, image1, image2 = compare_images(image_path1, image_path)
    print(f"Taux de compatibilité image {i}: {compatibility}")
    if compatibility > max_compatibility:
        max_compatibility = compatibility
        most_compatible = image2

# Afficher les images binaires pour comparaison visuelle
plt.subplot(1, 2, 1)
plt.imshow(image1, cmap='gray')
plt.title('Image 1 (binaire)')

plt.subplot(1, 2, 2)
plt.imshow(most_compatible, cmap='gray')
plt.title('Image 2 (binaire)')

plt.show()

