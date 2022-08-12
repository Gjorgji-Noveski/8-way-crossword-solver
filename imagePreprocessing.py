import cv2
import numpy as np


def preproces_image(img_path):

    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # numpy uses (height, width) as image shape order
    aspect_ratio = img_gray.shape[1]/img_gray.shape[0]
    # resizing the image so we the image size doesn't affect quality of image processing (blur, kernels, etc)
    img_resized = cv2.resize(img_gray, dsize=(int(500 * aspect_ratio), 500))

    blurred_img = cv2.blur(img_resized, (5, 5))
    hist_equal = cv2.equalizeHist(blurred_img)

    # thresh_img = cv2.bitwise_not(hist_equal) THIS OR THIS BELOW

    thresh_img = cv2.adaptiveThreshold(hist_equal, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 30)

    elipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # morph open
    morphed_elipse = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, elipse_kernel, iterations=8)

    # morph close
    morphed_elipse_close_inv = cv2.morphologyEx(morphed_elipse, cv2.MORPH_CLOSE, elipse_kernel, iterations=8)

    # morph erode
    # morphed_elipse_close_inv1 = cv2.morphologyEx(morphed_elipse_close_inv, cv2.MORPH_ERODE, elipse_kernel, iterations=8)

    cv2.imwrite('processed_image.jpg', thresh_img)
