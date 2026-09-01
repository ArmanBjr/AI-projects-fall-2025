# utility.py
#4021262459
#4021262131
from Board import Board
from player import Player

def utility(board: Board, player: Player, opponent: Player):
    player_count = board.count_pieces(player)
    opponent_count = board.count_pieces(opponent)

    is_game_finished = ( board.is_full() or (player.terminal_test(board) or opponent.terminal_test(board)))

    if is_game_finished:
        if (player_count > opponent_count) : return 10000
        elif (opponent_count > player_count) : return -10000
        else : return 0

    pieces_dif = player_count - opponent_count

    move_dif = len(player.getValidActions(board)) - len(opponent.getValidActions(board))
    move_dif_weight = 10

    top_left = board.board[0][0]
    top_right = board.board[0][board.column_count - 1]
    bottom_right = board.board[board.row_count - 1][board.column_count - 1]
    bottom_left = board.board[board.row_count - 1][0]

    player_number = player.number
    opponent_number = opponent.number

    isPlayer = 0

    if (top_left == player_number) :
        isPlayer += 1

    if (top_right == player_number) :
        isPlayer += 1    

    if (bottom_right == player_number) :
        isPlayer += 1

    if (bottom_left == player_number) :
        isPlayer += 1

        
    isOpponent = 0

    if (top_left == opponent_number) :
        isOpponent += 1

    if (top_right == opponent_number) :
        isOpponent += 1    

    if (bottom_right == opponent_number) :
        isOpponent += 1

    if (bottom_left == opponent_number) :
        isOpponent += 1


    pieces_dif_weight = 10
    player_corner_weight = 100
    # return 1
    return  pieces_dif * pieces_dif_weight + player_corner_weight * (isPlayer - isOpponent) + move_dif * move_dif_weight