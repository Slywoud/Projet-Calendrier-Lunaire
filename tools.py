import numpy as np
import cv2
from compare import binarize_image
from matplotlib import pyplot as plt
from scipy.optimize import minimize_scalar

def cropToCircle(img, x, y, radius):
    top_x = x - radius
    top_y = y - radius
    bot_x = x + radius
    bot_y = y + radius

    return img[top_y:bot_y, top_x:bot_x]

def rotation_image(image,degres):
    # Calculer le centre de l'image
    hauteur, largeur = image.shape[:2]
    centre_image = (largeur // 2, hauteur // 2)

    # Définir la matrice de rotation
    matrice_rotation = cv2.getRotationMatrix2D(centre_image, degres, 1.0)

    # Appliquer la rotation à l'image
    image_rotatee = cv2.warpAffine(image, matrice_rotation, (largeur, hauteur))

    return image_rotatee

def calculate_balance(img):
    img = binarize_image(img)
    width = img.shape[0]
    img_left = img[0:width, :round(width/2)]
    img_right = img[0:width, round(width/2):]
    pixels_left = cv2.countNonZero(img_left)
    pixels_right = cv2.countNonZero(img_right)

    return (pixels_left, pixels_right)

def straighten(img):
    baseline = calculate_balance(img)
    if baseline[0] > baseline [1]:
        # make it so left side has most possible white pixels and right has the least
        optimal = minimize_scalar(lambda x: calculate_balance(rotation_image(img, x))[1], method='Bounded',
                                  bounds=(-180, 180)).x
    else:
        optimal = minimize_scalar(lambda x: calculate_balance(rotation_image(img, x))[0], method='Bounded',
                                  bounds=(-180, 180)).x
    return rotation_image(img, optimal)


if __name__ == '__main__':
    img = cv2.imread('Images/phases/7.png')
    # img = cropToCircle(img, 246, 241, 207)
    img = rotation_image(img, 15)
    cv2.imshow('original', img)
    img = straighten(img)
    cv2.imshow('rotated', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
