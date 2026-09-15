# utility.py

from Board import Board
from player import Player

def utility(board: Board, player: Player, opponent: Player):
    # Todo
    player_count   = board.count_pieces(player)
    opponent_count = board.count_pieces(opponent)

    # Check if game is basically finished:
    # - board full OR both players have no moves
    player_moves   = player.getValidActions(board)
    opponent_moves = opponent.getValidActions(board)

    game_over = (
        board.is_full() or
        (len(player_moves) == 0 and len(opponent_moves) == 0)
    )

    if game_over:
        if player_count > opponent_count:
            return 10000   # big positive: win
        elif player_count < opponent_count:
            return -10000  # big negative: loss
        else:
            return 0       # draw

    # Not terminal: use heuristic
    piece_diff = player_count - opponent_count
    mobility_diff = len(player_moves) - len(opponent_moves)

    return piece_diff + 2 * mobility_diff

    pass
