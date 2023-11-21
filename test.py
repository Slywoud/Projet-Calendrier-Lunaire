import numpy as np
import cv2


def moon_finder(image_path='Images/Paysages/Ciel03.jpg'):
    contrast_value = 100

    while True:
        # Get an image from the file explorer
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        if image is None:
            print("Error: Could not read the image.")
            return []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, contrast = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=2, minDist=1000,
            param1=250, param2=70, minRadius=5, maxRadius=0)

        contrast_value += 10
        if contrast_value > 255:
            print("Error: Could not find circles.")
            return []

        # Display the image
        if circles is not None and len(circles[0]) == 1:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

            cv2.imshow('Detected Circle', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return [int(n) for n in circles[0][0]]


moon_finder()