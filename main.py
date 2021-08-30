import cv2
import numpy as np
import matplotlib.pyplot as plt
import subprocess
def preprocess(txt_path):
    import re
    with open(txt_path, mode='r', encoding='utf-8')as f:
        ocr_text_lines = [re.sub(r'[\W\d\s]', '', line).lower() for line in f.readlines() if line.strip() != '']
        ocr_text_lines = [line for line in ocr_text_lines if line!='']
    with open('data/after_preprocessing.txt', encoding='utf-8', mode='w') as wf:
        wf.write('\n'.join(ocr_text_lines))
    return ocr_text_lines


def check_element_exists(word_grid, coord):
    try:
        word_grid[coord[0]][coord[1]]
    except Exception:
        return False
    return True


def get_matching_coords(word_grid, coord, second_letter_to_search):
    row_nm = coord[0]
    col_nm = coord[1]

    matching_coordinates = [(row, col) for row in range(row_nm - 1, row_nm + 2) for col in range(col_nm - 1, col_nm + 2)
                            if check_element_exists(word_grid, (row, col)) and (row, col) != coord and
                            word_grid[row][col] == second_letter_to_search]
    return matching_coordinates


def get_direction(first_word_coord, second_word_coord):
    return (second_word_coord[0] - first_word_coord[0], second_word_coord[1] - first_word_coord[1])


def search_till_end(word_grid, curr_coord, direction, search_word):
    found_coords = []
    for letter in search_word:
        curr_coord = (curr_coord[0] + direction[0], curr_coord[1] + direction[1])
        if check_element_exists(word_grid, curr_coord):
            if word_grid[curr_coord[0]][curr_coord[1]] == letter:
                found_coords.append(curr_coord)
                continue
        break
    else:
        return found_coords
    return []


def loop_through_letters(word_grid, search_word):
    for row_idx, row in enumerate(word_grid):
        for col_idx, curr_letter in enumerate(row):
            if curr_letter == search_word[0]:
                match_coords = get_matching_coords(word_grid, (row_idx, col_idx), search_word[1])
                for coord in match_coords:
                    direction = get_direction((row_idx, col_idx), coord)
                    found_coords = search_till_end(word_grid, (row_idx, col_idx), direction, search_word[1:])
                    if found_coords:
                        found_coords.insert(0, (row_idx, col_idx))
                        print(found_coords)

def ocr(path):
    # img = cv2.imread(path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def show_pic(img, gray=False):
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(111)
        if gray:
            ax.imshow(img, cmap='gray')
        else:
            ax.imshow(img)

    # Blur
    blurred_img = cv2.blur(img_gray, (11, 11))
    # show_pic(blurred_img, gray=True)

    # OTSU Thresh (finds value for binary thresh automatically, the value is a minimal value of the peaks of the histogram (peak for dark colors and light colors)
    # basically the furhtest peak to the left and furthest to the right finds the value that has the minimal variance between them.
    ret, thresh_img = cv2.threshold(blurred_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # show_pic(thresh_img, gray=True)

    # Morphology operators
    thresh_img = cv2.bitwise_not(thresh_img)
    elipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # open
    morphed_elipse = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, elipse_kernel, iterations=4)
    # show_pic(morphed_elipse, True)

    # close
    morphed_elipse_close_inv = cv2.morphologyEx(morphed_elipse, cv2.MORPH_CLOSE, elipse_kernel, iterations=3)
    # show_pic(morphed_elipse_close_inv, True)

    # Erode
    morphed_elipse_close_inv1 = cv2.morphologyEx(morphed_elipse_close_inv, cv2.MORPH_ERODE, elipse_kernel, iterations=4)
    # show_pic(morphed_elipse_close_inv1, True)

    # saving img
    cv2.imwrite('data/processed_word_grid.jpg', morphed_elipse_close_inv1)



ocr('data/krstozbor (1).jpg')
subprocess_result = subprocess.run(['tesseract', 'data/processed_word_grid.jpg', 'data/tesseract_text', '-l', 'mkd', '-psm', '11'], capture_output=True, text=True)
print(f'Stdout: {subprocess_result.stdout}')
print(f'Stderr: {subprocess_result.stderr}')
#
matrix = preprocess(r'data/tesseract_text.txt')
loop_through_letters(matrix, 'канада')

# subprocess_result = subprocess.run(['tesseract', 'data/processed_word_gird.jpg', 'data/tesseract_text', '-l', 'mkd', '-psm', '11'], capture_output=True, text=True)
# print(f'Stdout: {subprocess_result.stdout}')
# print(f'Stderr: {subprocess_result.stderr}')