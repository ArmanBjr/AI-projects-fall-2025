from Block import Block
from Board import Board


class Action:

    @staticmethod
    def up(block: Block, board: Board):
        board.gird[block.position[block.last_position - 1][0]][block.position[block.last_position - 1][1]] = 0
        for i in range(block.last_position):
            block.position[i][0] -= 1
        board.gird[block.position[0][0]][block.position[0][1]] = board.gird[block.position[1][0]][block.position[1][1]]

    @staticmethod
    def down(block: Block, board: Board):
        board.gird[block.position[0][0]][block.position[0][1]] = 0
        for i in range(block.last_position):
            block.position[i][0] += 1
        board.gird[block.position[block.last_position - 1][0]][block.position[block.last_position - 1][1]] = board.gird[block.position[0][0]][block.position[0][1]]

    @staticmethod
    def left(block: Block, board: Board):
        board.gird[block.position[block.last_position - 1][0]][block.position[block.last_position - 1][1]] = 0
        for i in range(block.last_position):
            block.position[i][1] -= 1
        board.gird[block.position[0][0]][block.position[0][1]] = board.gird[block.position[1][0]][block.position[1][1]]

    @staticmethod
    def right(block: Block, board: Board):
        board.gird[block.position[0][0]][block.position[0][1]] = 0
        for i in range(block.last_position):
            block.position[i][1] += 1
        board.gird[block.position[block.last_position - 1][0]][block.position[block.last_position - 1][1]] = board.gird[block.position[0][0]][block.position[0][1]]
