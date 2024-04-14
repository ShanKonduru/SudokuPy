import random

class Sudoku:
    def __init__(self, level='simple'):
        self.level = level
        self.board = self.generate_board()
        self.solved_board = self.solve_board(self.board)

    def generate_board(self):
        board = [[0]*9 for _ in range(9)]
        self.solve(board)
        self.remove_numbers(board)
        return board

    def solve(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(board, i, (row, col)):
                board[row][col] = i

                if self.solve(board):
                    return True

                board[row][col] = 0

        return False

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        # Check row
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def remove_numbers(self, board):
        level_to_remove = {
            'simple': 40,
            'medium': 50,
            'complex': 60
        }
        to_remove = level_to_remove[self.level]

        while to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if board[row][col] != 0:
                board[row][col] = 0
                to_remove -= 1

    def solve_board(self, board):
        solved_board = [row[:] for row in board]
        self.solve(solved_board)
        return solved_board

    def print_board(self, board):
        for i in range(len(board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")

            for j in range(len(board[i])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")

                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")

    def play(self):
        print("Sudoku Game - Level: {}".format(self.level.capitalize()))
        self.print_board(self.board)
        print("\nEnter row, column and number (e.g., '3 4 5') or 'quit' to exit:")

        while True:
            user_input = input("> ")

            if user_input.lower() == 'quit':
                print("Goodbye!")
                break

            try:
                row, col, num = map(int, user_input.split())
                if self.is_valid(self.board, num, (row-1, col-1)):
                    self.board[row-1][col-1] = num
                    self.print_board(self.board)

                    if self.board == self.solved_board:
                        print("\nCongratulations! You solved the Sudoku!")
                        break
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Invalid input! Please enter row, column and number.")

if __name__ == "__main__":
    level = input("Choose a level (simple, medium, complex): ").lower()
    while level not in ['simple', 'medium', 'complex']:
        level = input("Invalid level! Choose a level (simple, medium, complex): ").lower()

    game = Sudoku(level)
    game.play()
