import copy

class TextProcessing:

    def __init__(self, textPath):
        self.textPath = textPath

    def text_process(self, txt_path):
        import re
        with open(txt_path, mode='r', encoding='utf-8')as f:
            ocr_text_lines = [re.sub(r'[\W\d\s]', '', line).lower() for line in f.readlines() if line.strip() != '']
            ocr_text_lines = [line for line in ocr_text_lines if line != '']
        with open("after_processing.txt", encoding='utf-8', mode='w') as wf:
            wf.write('\n'.join(ocr_text_lines))
        return ocr_text_lines

    def check_element_exists(self, word_grid, coord):
        try:
            word_grid[coord[0]][coord[1]]
        except Exception:
            return False
        return True

    def get_matching_coords(self, word_grid, coord, second_letter_to_search):
        row_nm = coord[0]
        col_nm = coord[1]

        matching_coordinates = [(row, col) for row in range(row_nm - 1, row_nm + 2) for col in
                                range(col_nm - 1, col_nm + 2)
                                if self.check_element_exists(word_grid, (row, col)) and (row, col) != coord and
                                word_grid[row][col] == second_letter_to_search]
        return matching_coordinates

    def get_direction(self, first_word_coord, second_word_coord):
        return (second_word_coord[0] - first_word_coord[0], second_word_coord[1] - first_word_coord[1])

    def search_till_end(self, word_grid, curr_coord, direction, search_word):
        found_coords = []
        for letter in search_word:
            curr_coord = (curr_coord[0] + direction[0], curr_coord[1] + direction[1])
            if self.check_element_exists(word_grid, curr_coord):
                if word_grid[curr_coord[0]][curr_coord[1]] == letter:
                    found_coords.append(curr_coord)
                    continue
            break
        else:
            return found_coords
        return []

    def create_result_text(self, word_grid, locations):
        wg = copy.copy(word_grid)
        if locations[0][0] == locations[-1][0] and locations[0][1] < locations[-1][1]:
            locations.reverse()  # if the found match is a horizontal one, going left to right, the code will put multiple "()" at the same place because the string changes when parenthesis are inserted, reverse fixes it
        for loc in locations:
            wg[loc[0]] = wg[loc[0]][:loc[1]] + '(' + wg[loc[0]][loc[1]] + ')' + wg[loc[0]][loc[1] + 1:]
        result = ""
        result += '\n'.join(wg)
        result += '\n---------------\n'
        return result
    
    def loop_through_letters(self, word_grid, word):
        result_text = []
        for row_idx, row in enumerate(word_grid):
            for col_idx, curr_letter in enumerate(row):
                if curr_letter == word[0]:
                    match_coords = self.get_matching_coords(word_grid, (row_idx, col_idx), word[1])
                    for coord in match_coords:
                        direction = self.get_direction((row_idx, col_idx), coord)
                        found_coords = self.search_till_end(word_grid, (row_idx, col_idx), direction, word[1:])
                        if found_coords:
                            found_coords.insert(0, (row_idx, col_idx))

                            result_text.append(self.create_result_text(word_grid, found_coords))
        return "\n".join(result_text)


    def search(self, word):
        matrix = self.text_process(self.textPath)
        return self.loop_through_letters(matrix, word)
