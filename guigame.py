import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 540, 600
CELL_SIZE = WIDTH // 9

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)

class Sudoku:
    def __init__(self, level='simple'):
        self.level = level
        self.board = self.generate_board()
        self.solved_board = self.solve_board()

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

    def solve_board(self):
        solved_board = [row[:] for row in self.board]
        self.solve(solved_board)
        return solved_board

    def draw_board(self, screen):
        for i in range(9):
            for j in range(9):
                cell = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, cell, 1)

                if self.board[i][j] != 0:
                    text_surface = FONT.render(str(self.board[i][j]), True, BLACK)
                    text_rect = text_surface.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text_surface, text_rect)

    def draw_selected_cell(self, screen, row, col):
        cell = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLUE, cell, 3)

    def draw_error(self, screen, row, col):
        cell = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, cell, 3)

    def play(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Sudoku')

        selected = None
        running = True
        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    if 0 <= row < 9 and 0 <= col < 9 and self.board[row][col] == 0:
                        selected = (row, col)
                    else:
                        selected = None

                if event.type == pygame.KEYDOWN:
                    if selected:
                        if event.unicode.isdigit() and self.is_valid(self.board, int(event.unicode), selected):
                            self.board[selected[0]][selected[1]] = int(event.unicode)
                            selected = None
                        elif event.key == pygame.K_RETURN:
                            row, col = selected
                            if self.board[row][col] == self.solved_board[row][col]:
                                self.draw_selected_cell(screen, row, col)
                            else:
                                self.draw_error(screen, row, col)
                        elif event.key == pygame.K_BACKSPACE:
                            self.board[selected[0]][selected[1]] = 0
                            selected = None

            self.draw_board(screen)

            if selected:
                self.draw_selected_cell(screen, *selected)

            if self.board == self.solved_board:
                self.draw_success(screen)

            pygame.display.update()

    def draw_success(self, screen):
        text_surface = FONT.render("Congratulations! Sudoku Solved!", True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    level = input("Choose a level (simple, medium, complex): ").lower()
    while level not in ['simple', 'medium', 'complex']:
        level = input("Invalid level! Choose a level (simple, medium, complex): ").lower()

    game = Sudoku(level)
    game.play()
