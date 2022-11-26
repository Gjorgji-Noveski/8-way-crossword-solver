import cv2


class ImgPreprocessing:
    """
    In order to account for different sized word grids, a ratio is calculated between the width of the image
    and the number of columns in the word grid. This ratio is used to calculate the width of the resized image.
    During testing the ratio of 52 was found to be a good default (500 pixels image width / 10 columns in the word grid)
    So for example, if the image contains 15 columns, we rescale the input image to a width of around 765 (15*51)
    """

    ratio = 52

    @classmethod
    def calc_dim_with_aspect_ratio(cls, img_shape, col_count):
        # numpy uses (height, width) as image shape order. The image opened with OpenCV are stored as numpy array
        aspect_ratio = img_shape[1] / img_shape[0]
        size = int((cls.ratio * col_count) / aspect_ratio)

        new_dim = int(size * aspect_ratio), size
        return new_dim

    @classmethod
    def preproces_image(cls, img_path, col_count):
        img_color = cv2.imread(img_path)
        # used just for displaying on interface
        img_color_resized = cv2.resize(img_color,
                                       dsize=cls.calc_dim_with_aspect_ratio(img_color.shape, col_count))
        print(f'original size {img_color.shape}\nresized: {img_color_resized.shape}')

        cv2.imwrite('resized_image.jpg', img_color_resized)

        img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        """
        This is done to ensure that we always have consistent amount of preprocessing done to the image, regardless of the
        image size. For example if we don't resize the image, running one blur iteration on a 1200x600 image will have a
        weaker effect than running the one blur iteration on a 800x400 image and thus quality of the optical character 
        recognition will vary.
        """
        img_resized = cv2.resize(img_gray, dsize=cls.calc_dim_with_aspect_ratio(img_gray.shape, col_count))

        blurred_img = cv2.blur(img_resized, (5, 5))

        thresh_img = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 15)

        # We are doing this because for morphological operators, opencv considers the white color as foreground if we don't
        # do this, our morphological operators will be flipped (erode will do dilation, and vice versa)
        thresh_img = cv2.bitwise_not(thresh_img)

        elipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        # morph open
        morphed_elipse = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, elipse_kernel, iterations=1)

        # to make letters black again
        final_img = cv2.bitwise_not(morphed_elipse)

        cv2.imwrite('processed_image.jpg', final_img)


"""
Notes:
- histogram equalization seemed to make the ocr detection worse. Without it the lines between the letters are almost gone(which is good)
- Not many morphological operators were needed as in the begginning, just opening to remove some noise from the surrounding area.
- tesseract psm 6 seemed to be a bit better, since it searches for a uniform block of text, whilest psm 11 searches everywhere for letters,
meaning it can even return (falsely) letters which are outside the word grid
"""
