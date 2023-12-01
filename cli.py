from tools import *
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=str, help='The filepath for the image to analyse')
parser.add_argument('-c', '--cropped', type=bool, default=False, help='show the cropped image')
parser.add_argument('-s', '--straighten', type=bool, default=False, help='show straightened image')
parser.add_argument('-b', '--binarized', type=bool, default=False, help='show binarized image')
parser.add_argument('-m', '--highlighted', type=bool, default=False, help='show the the image with the moon highlighted')
args = parser.parse_args()

image = cv2.imread(args.filepath)
moon_coords = moon_coordinates(image)
cropped = crop_to_circle(image, moon_coords[0], moon_coords[1], moon_coords[2])
if args.cropped:
    cv2.imshow('cropped', cropped)
straightened = straighten(cropped)
if args.straighten:
    cv2.imshow('straightened', straightened)
if args.binarized:
    cv2.imshow('binarized', binarize_image(straightened))
sim_phase, sim_phase_name, similarity = get_most_similar(straightened, 'Images/phases')
if args.highlighted:
    cv2.imshow('highlighted moon', circle_display_on_image(image, moon_coords))

fig, axs = plt.subplots(nrows=1, ncols=2)

axs[0].imshow(circle_display_on_image(image, moon_coords))
axs[1].imshow(sim_phase)
print(moon_coords)
plt.show()
cv2.waitKey(0)