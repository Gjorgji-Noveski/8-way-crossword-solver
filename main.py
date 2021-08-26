def preprocess(txt_path):
    import re
    with open(txt_path, mode='r', encoding='utf-8')as f:
        ocr_text_lines = [re.sub(r'[\W\d\s]', '', line).lower() for line in f.readlines() if line.strip() != '']

    return ocr_text_lines


def store_letters_in_dict(txt_lines):
    letter_loc_dict = {}
    for line_idx, line in enumerate(txt_lines):
        for char_idx, letter in enumerate(line):
            loc = (line_idx, char_idx)
            if letter not in letter_loc_dict:
                letter_loc_dict[letter] = []
                letter_loc_dict[letter].append(loc)
            else:
                letter_loc_dict[letter].append(loc)
    return letter_loc_dict


# current_letter_idx = 0
# letter_loc_dict = store_letters_in_dict(preprocess(r'PATH'))
# visited_locs = []


def find_words(words):
    global letter_loc_dict
    for word in words:
        first_letter_stack = letter_loc_dict[word[0]].copy()

        while first_letter_stack:
            current_loc = first_letter_stack.pop()
            continuing(current_loc, word)


def continuing(current_loc, word):
    global current_letter_idx, letter_loc_dict, visited_locs
    flag_found_smth = False

    next_letter_stack = letter_loc_dict[word[current_letter_idx]].copy()
    while next_letter_stack:
        loc2 = next_letter_stack.pop()
        # ako najde
        # print(type(current_loc))
        # print(type(loc2))
        # print(current_loc)
        # print(loc2)
        check_closeness_mapper = map(lambda tup1, tup2: abs(tup1[0] - tup2[0]) <= 1 and abs(tup1[1] - tup2[1]) <= 1,
                                     [current_loc], [loc2])
        if list(check_closeness_mapper)[0]:
            print(loc2)
            current_letter_idx += 1
            flag_found_smth = True
            continuing((loc2), word)
    # ako ne najde
    if not flag_found_smth:
        current_letter_idx -= 1


def compare_locs(curr_letter_locs, next_letter_locs):
    # turi mu iterable od 1 tuple samo
    for cr_loc in curr_letter_locs:
        for nx_loc in next_letter_locs:
            # check in 8 directions if the next letter is present
            check_closeness_mapper = map(lambda tup1, tup2: abs(tup1[0] - tup2[0]) <= 1 and abs(tup1[1] - tup2[1]) <= 1,
                                         [cr_loc], [nx_loc])
            if list(check_closeness_mapper)[0] == True:
                return nx_loc
    return False


# current_letter_idx = 0
# lines = ['ksqasamd','suqasdas','asqasdjs','asqbsdks','asdardes','asdarels']
#
# letter_loc_dict = store_letters_in_dict(lines)
# print(letter_loc_dict)
# find_words(['qqqq'])
# TODO: NAPRAI FUNCKIJA SHTO KE GO PRETVORAT VO nxn GRID liniite od OCR-ot, deka nekad mozhda da dobieme samo edna bukva vo eden red a vo svite drugi po 5 turi go kaj ifoivte na list comprehensionov
# TODO: ama komplicirano e, neka bide samo taka raw od ocr i da ima funck shto ke proveruva dali ima element

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
    najdeni_coords = []
    for letter in search_word:
        curr_coord = (curr_coord[0] + direction[0], curr_coord[1] + direction[1])
        if check_element_exists(word_grid, curr_coord):
            if word_grid[curr_coord[0]][curr_coord[1]] == letter:
                najdeni_coords.append(curr_coord)
                continue
        break
    else:
        return najdeni_coords
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
                        print(found_coords)


matrix = preprocess(r'C:\Users\dis\Desktop\krstozbor_procesiran - Copy.txt')
loop_through_letters(matrix, 'lepak')

