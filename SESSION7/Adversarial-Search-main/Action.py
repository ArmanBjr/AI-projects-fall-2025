# Action.py

from __future__ import annotations

from Board import Board

class Action:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

def doAction(action: Action, player: Player, board: Board):
    r, c = action.row, action.col
    if board.board[r][c] != Board.EMPTY:
        raise ValueError("Invalid: Position not empty")

    opponent_num = 3 - player.number
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    flips = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        path = []
        while 0 <= nr < board.row_count and 0 <= nc < board.column_count:
            if board.board[nr][nc] == opponent_num:
                path.append((nr, nc))
                nr += dr
                nc += dc
            elif board.board[nr][nc] == player.number and path:
                flips.extend(path)
                break
            else:
                break

    if not flips:
        raise ValueError("Invalid: No flips")

    # Place piece
    board.board[r][c] = player.number

    # Flip pieces
    for fr, fc in flips:
        board.board[fr][fc] = player.number