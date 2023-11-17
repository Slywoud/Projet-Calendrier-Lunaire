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
    # Convertir les images en niveaux de gris
    img1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculer le SSIM
    similarity_index, _ = ssim(img1_gray, img2_gray, full=True)

    return similarity_index

# Exemple d'utilisation
image_path1 = "Images/Paysages/Ciel03-edit.jpg"
image_path2 = "Images/phases/7.png"

# Charger et redimensionner les images
img1, img2 = resize_images(image_path1, image_path2)

# Calculer le SSIM
compatibility = compare_images(img1, img2)
print(f"Taux de compatibilité : {compatibility}")

# Afficher les images pour comparaison visuelle (facultatif)
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
plt.title('Image 1')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
plt.title('Image 2')

plt.show()
