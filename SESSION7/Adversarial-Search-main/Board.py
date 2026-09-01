# Board.py

class Board:
    EMPTY = 0
    BLOCK = 3

    def __init__(self, row_count: int, column_count: int, center_block: bool):
        self.row_count = row_count
        self.column_count = column_count
        self.board = [[self.EMPTY for _ in range(column_count)] for _ in range(row_count)]

        # Initial setup for Othello
        mid1 = row_count // 2 - 1
        mid2 = row_count // 2
        self.board[mid1][mid1] = 2  # White
        self.board[mid1][mid2] = 1  # Black
        self.board[mid2][mid1] = 1  # Black
        self.board[mid2][mid2] = 2  # White

        if center_block:
            # Not used for Othello, but for compatibility
            center_r = row_count // 2
            center_c = column_count // 2
            self.board[center_r][center_c] = self.BLOCK

    def draw_board(self):
        symbols = {
            self.EMPTY: '.',
            1: 'X',
            2: 'O',
            self.BLOCK: '#'
        }
        for row in self.board:
            print(' '.join(symbols[cell] for cell in row))
        print()

    def count_pieces(self, player):
        return sum(
            1 for row in self.board for cell in row if cell == player.number
        )

    def is_full(self):
        return all(cell != self.EMPTY for row in self.board for cell in row)