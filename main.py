import itertools

# Constants
BOARD_SIZE = 15

with open('dictionary.txt', 'r') as words_file:
    WORD_LIST = set(words_file.read().splitlines())


# Scrabble Board Class
class ScrabbleBoard:
    def __init__(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def place_word(self, word, row, col, direction):
        for i, letter in enumerate(word):
            if direction == "H":  # Horizontal
                self.board[row][col + i] = letter
            else:  # Vertical
                self.board[row + i][col] = letter

    def display(self):
        for row in self.board:
            print(' '.join(row))


# Trie for Fast Word Lookups
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word


# Generate Possible Words
def generate_words(tiles, trie):
    words = set()
    for i in range(1, len(tiles) + 1):
        for perm in itertools.permutations(tiles, i):
            word = ''.join(perm)
            if trie.search(word):
                words.add(word)
    return words


# Board Evaluation Function
def evaluate_board(board):
    score = 0
    letter_values = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
        'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
        'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
        'Y': 4, 'Z': 10
    }
    for row in board.board:
        for letter in row:
            if letter != ' ':
                score += letter_values.get(letter, 0)
    return score


# Get All Possible Moves
def get_all_moves(board, tiles, trie):
    moves = []
    possible_words = generate_words(tiles, trie)
    for word in possible_words:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE - len(word) + 1):
                if all(board.board[row][col + i] in (' ', letter) for i, letter in enumerate(word)):
                    moves.append((word, row, col, "H"))
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE - len(word) + 1):
                if all(board.board[row + i][col] in (' ', letter) for i, letter in enumerate(word)):
                    moves.append((word, row, col, "V"))
    return moves


# Apply a Move to the Board
def apply_move(board, move):
    new_board = ScrabbleBoard()
    new_board.board = [row[:] for row in board.board]  # Copy board
    word, row, col, direction = move
    new_board.place_word(word, row, col, direction)
    return new_board


# Minimax with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, is_maximizing, tiles, trie):
    if depth == 0:
        return evaluate_board(board)

    moves = get_all_moves(board, tiles, trie)  # Ensure correct call
    if not moves:  # No moves available
        return evaluate_board(board)

    if is_maximizing:
        best_score = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            score = minimax(new_board, depth - 1, alpha, beta, False, tiles, trie)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            score = minimax(new_board, depth - 1, alpha, beta, True, tiles, trie)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score


# AI Move Selection
def find_best_move(board, tiles, trie):
    best_move = None
    best_score = float('-inf')

    moves = get_all_moves(board, tiles, trie)  # Ensure valid move list
    if not moves:  # No moves available
        return None

    for move in moves:
        new_board = apply_move(board, move)
        score = minimax(new_board, 2, float('-inf'), float('inf'), False, tiles, trie)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

# Main Function
def main():
    board = ScrabbleBoard()
    trie = Trie()
    for word in WORD_LIST:
        trie.insert(word.strip().upper())

    tiles = ["C", "A", "T", "D", "O", "G", "M"]  # Example tiles
    best_move = find_best_move(board, tiles, trie)
    if best_move:
        word, row, col, direction = best_move
        board.place_word(word, row, col, direction)

    board.display()


if __name__ == "__main__":
    main()
