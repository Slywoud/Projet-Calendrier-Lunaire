import numpy as np
import cv2
from tkinter import filedialog
import tkinter as tk


def moon_coordinates(img):
    contrast_value = 100

    image = cv2.imread(img, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Réduction du bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Détermination d'un seuil adaptatif
    _, contrast = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=2, minDist=1000,
        param1=250, param2=70, minRadius=5, maxRadius=0)

    contrast_value += 10
    if contrast_value > 255 or circles is None or len(circles[0]) != 1:
        print("Erreur : Impossible de trouver la lune.")
        return None

    return circles, image


def circle_display_on_image(image, circles):
    if circles is not None and len(circles[0]) == 1:
        image_with_circles = image.copy()

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(image_with_circles, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(image_with_circles, (i[0], i[1]), 2, (0, 0, 255), 3)

        return image_with_circles

    return None


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    img = filedialog.askopenfilename(title="Sélectionnez une image",
                                     filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg")])

    circles, image = moon_coordinates(img)
    print("Coordonnées du cercle :", circles)

    final_image = circle_display_on_image(image, circles)
    cv2.imshow('Final Image', final_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()