import numpy as np
import cv2
from tkinter import filedialog
import tkinter as tk


def moon_finder():
    contrast_value = 100
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Sélectionnez une image",
                                           filetypes=[("Fichiers image", "*.png;*.jpg;*.jpeg")])

    # Check si un fichier a été choisi
    if not file_path:
        print("Erreur : Aucun fichier sélectionné.")
        return []

    image = cv2.imread(file_path, cv2.IMREAD_COLOR)

    if image is None:
        print("Erreur : Impossible de lire l'image.")
        return []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Réduction du bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Détermination d'un seuil adaptatif
    _, contrast = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=2, minDist=1000,
        param1=250, param2=70, minRadius=5, maxRadius=0)

    contrast_value += 10
    if contrast_value > 255:
        print("Erreur : Impossible de trouver la lune.")
        return []

    # Affiche l'image
    if circles is not None and len(circles[0]) == 1:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Cercle original
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

            # Définir une région d'intérêt (ROI) autour du cercle détecté
            x, y, r = i[0], i[1], i[2]

            # Ajuster les limites de la ROI pour éviter les indices négatifs ou dépassant les dimensions de l'image
            roi_x_start = max(0, x - r)
            roi_x_end = min(image.shape[1], x + r)
            roi_y_start = max(0, y - r)
            roi_y_end = min(image.shape[0], y + r)

            roi = image[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

            # Zoom sur la ROI
            if roi.shape[0] > 0 and roi.shape[1] > 0:
                zoomed_roi = cv2.resize(roi, (2 * r, 2 * r))
                cv2.imshow('Zoomed Circle', zoomed_roi)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("Erreur : La ROI est vide.")
                return []

        return [int(n) for n in circles[0][0]]


moon_finder()