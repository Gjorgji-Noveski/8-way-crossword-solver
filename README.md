search_half_word is a functionality that for a given search word
it searches the grid of the two "half" words that make up the search word.

For example if the search word is "skyscraper", then with that option on
the algorithm will search for the word "skysc" and "raper". This is in case the ocr
didn't yield good results, and the final grid is not a correct NxN grid, but maybe a 
NxN+1 grid.