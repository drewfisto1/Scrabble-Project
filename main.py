from values import values

DICTIONARY_FILE = "dictionary.txt"

def user_tiles():
    tiles = input("What letters do you have?")
    tiles = tiles.upper()
    tiles_list = []

    for tile in tiles:
        if tile.isalpha():
            tiles_list.append(tile)

        
    return tiles_list

def find_valid_words(letters):
    with open(DICTIONARY_FILE, "r") as dictionary_file:
        dictionary_lines = dictionary_file.readlines()
        tile_char_occurences = char_occurences(letters)
        valid_words = []
       
        for line in dictionary_lines:
            valid_word = True
            line = line.rstrip('\n')
            dict_char_occurences = char_occurences(line)

            for char in line:                     
                if dict_char_occurences[char] > tile_char_occurences.get(char, 0):
                    valid_word = False
                    break

            if valid_word:
                valid_words.append(line)

    return valid_words
                            
def find_best_word(words):
    best_words = {}

    for word in words:
        amount = 0
        for char in word:
            amount += values[char]

        best_words[word] = amount
    
    max_value = max(best_words.values())
    best_word = {word: score for word, score in best_words.items() if score == max_value}

    return best_word


def char_occurences(data):   
    char_dict = {}
    for char in data:
        if char in char_dict:
            char_dict[char] += 1
        else:
            char_dict[char] = 1

    return char_dict

def main():
    tiles = user_tiles()
    valid_words = find_valid_words(tiles)
    
    if not valid_words:
        print("No valid words, WOMP WOMP")
    else:
        best_word = find_best_word(valid_words)
        print(best_word)

if __name__ == "__main__":
    main() 


                

