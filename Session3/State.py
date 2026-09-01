# this class only for the first time setup init state for problem and is given to every search
from Board import Board


class State:
    def __init__(self, board: Board, parent, g_n: int, direction: str, piece: int):
        self.board = board
        self.parent = parent
        self.g_n = g_n
        self.direction = direction
        self.piece = piece
        self.__f_limit = float("inf")

    def __hash__(self):
        return self.board.__hash__()

    def __lt__(self, other):
        return True

    def h_n(self):
        b = self.board
        x0, y0 = b.red_block.position[0]
        x1, y1 = b.red_block.position[1]
        h = (b.width - 1) - y1
        blockers = set()
        for c in range(y1 + 1, b.width):
            val = b.gird[x0][c]
            if val != 0:
                blockers.add(val)
        blockers.discard(0) 
        blockers.discard(-1)
        final_h = h + len(blockers)
        return final_h

    def f_n(self, is_rbfs=False):
        if is_rbfs:
            return min(self.g_n + self.h_n(), self.__f_limit)
        return self.g_n + self.h_n()

    def set_f_limit(self, value):
        self.__f_limit = value
