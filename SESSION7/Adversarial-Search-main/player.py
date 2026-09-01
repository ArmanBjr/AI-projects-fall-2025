# player.py

from Board import Board
from Action import Action

class Player:
    def __init__(self, number: int):
        self.number = number

    def getValidActions(self, board: Board):
        actions = []
        opponent_num = 3 - self.number
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for r in range(board.row_count):
            for c in range(board.column_count):
                if board.board[r][c] != Board.EMPTY:
                    continue
                flips = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    has_opponent = False
                    while 0 <= nr < board.row_count and 0 <= nc < board.column_count:
                        if board.board[nr][nc] == opponent_num:
                            has_opponent = True
                            nr += dr
                            nc += dc
                        elif board.board[nr][nc] == self.number and has_opponent:
                            flips = True
                            break
                        else:
                            break
                if flips:
                    actions.append(Action(r, c))
        return actions

    def terminal_test(self, board: Board) -> bool:
        return len(self.getValidActions(board)) == 0