import cv2
from scipy.optimize import minimize_scalar
from skimage.metrics import structural_similarity as ssim
import os

def crop_to_circle(img, x, y, radius):
    '''
    Takes an image and the coordinates of a circle on the image and returns an image cropped to that circle
        Paremeters:
            img (numpy array): the image to be cropped
            x (int): the x coordinate of the center of the circle to crop down to
            y (int): the y coordinate of the center of the circle to crop down to
            radius (int): the radius of the circle to crop down to

        Returns:
            img (numpy array): the image cropped down to a square of width 2*radius centered around the circle
    '''
    top_x = x - radius
    top_y = y - radius
    bot_x = x + radius
    bot_y = y + radius

    return img[top_y:bot_y, top_x:bot_x]

def rotate_image(image, degrees):
    '''
    Takes an image and the number of the degrees to rotate the image by
        Paremeters:
            img (numpy array): the image to be rotated
            degrees (int): the number of degrees by which to rotate the image

        Returns:
            img (numpy array): the rotated image
    '''
    # Calculate the centre of the image
    hauteur, largeur = image.shape[:2]
    centre_image = (largeur // 2, hauteur // 2)

    # Define the rotation matrix
    matrice_rotation = cv2.getRotationMatrix2D(centre_image, degrees, 1.0)

    # Rotate the image
    image_rotatee = cv2.warpAffine(image, matrice_rotation, (largeur, hauteur))

    return image_rotatee

def calculate_balance(img, thresh_value=50):
    '''
    Returns the number of pixels above a given threshold on the left and right half of an image
        Paremeters:
            img (numpy array): the image to be cropped
            thresh_value (int) : the value of the threshold above which to count pixels, by default the value is 50

        Returns:
            (pixels_left, pixels_right) (tuple of two ints): the number of pixels above the threshold on each side of the image
    '''
    img = binarize_image(img, thresh_value)
    width = img.shape[0]
    img_left = img[0:width, :round(width/2)]
    img_right = img[0:width, round(width/2):]
    pixels_left = cv2.countNonZero(img_left)
    pixels_right = cv2.countNonZero(img_right)

    return (pixels_left, pixels_right)

def straighten(img):
    '''
    Takes an image of a moon and attempts to straighten the image so that the moon is vertical
        Paremeters:
            img (numpy array): the image to be straightened

        Returns:
            img (numpy array): the image cropped down to a square of width 2*radius centered around the circle
    '''
    baseline = calculate_balance(img)
    if baseline[0] > baseline[1]:
        # make it so left side has most possible white pixels and right has the least
        optimal = minimize_scalar(lambda x: calculate_balance(rotate_image(img, x))[1], method='Bounded',
                                  bounds=(-180, 180)).x
    else:
        optimal = minimize_scalar(lambda x: calculate_balance(rotate_image(img, x))[0], method='Bounded',
                                  bounds=(-180, 180)).x
    return rotate_image(img, optimal)

def match_image_sizes(img_to_match, img_to_resize):
    '''
    Takes two images and resizes one to match the other
        Paremeters:
            img_to_match (numpy array): the image whose dimensions should be matched
            img_to_resize (numpy array): the image whose dimensions will be changed

        Returns:
            img (numpy array): the resized image
    '''
    # Redimensionner les images pour qu'elles aient la même taille
    return cv2.resize(img_to_resize, (img_to_match.shape[1], img_to_match.shape[0]))

def binarize_image(image, thresh_value=50):
    '''
    Returns a binary version of the image
        Paremeters:
            img (numpy array): the image to be filtered
            thresh_value (int): the value of the threshold for the binary filter

        Returns:
            img (numpy array): the filtered image
    '''
    img1_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, img1_binary = cv2.threshold(img1_gray, thresh_value, 255, cv2.THRESH_BINARY)

    return img1_binary

def compare_images(image1, image2):
    '''
    Returns the similiraty index of two images
        Paremeters:
            image1 (numpy array): the first image to compare
            image2 (numpy array): the second image to compare

        Returns:
            similarity_index (float): value from 0.0 to 1.0 representing the similarity of the two images
    '''
    # Calculer le SSIM
    image1 = match_image_sizes(image2, image1)
    image1 = binarize_image(image1)
    image2 = binarize_image(image2)
    similarity_index, _ = ssim(image1, image2, full=True)
    return similarity_index

def get_most_similar(image, folder_path):
    '''
    Returns information relating to the most similar image in a folder to the one given
        Paremeters:
            image (numpy array): the image to compare
            folder_path (string): the path to the folder containing the images to compare to

        Returns:
            most_similar (numpy array): the most compatible image in the target folder
            most_similar_name (string): the name of the most compatible image
            max_similarity (float): the similarity index of the most similar image
    '''
    most_similar = ''
    most_similar_name = ''
    max_similarity = 0.0
    for img in os.listdir(folder_path):  # Images numérotées de 0 à 28
        phase_path = os.path.join(folder_path, img)
        print(phase_path)
        phase = cv2.imread(phase_path)
        similarity = compare_images(image, phase)

        print(f"Taux de compatibilité image {img}: {similarity}")
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar = phase
            most_similar_name = f"Phase : {img}"

    return most_similar, most_similar_name, max_similarity

if __name__ == '__main__':
    image = cv2.imread('Images/phases/7.png')
    print(get_most_similar(image, 'Images/phases/'))