# main.py

from player import Player
from Board import Board
from Adversarial_Search import AI
from Action import doAction

depth = 7
player1 = Player(1)  # Black
player2 = Player(2)  # White
board = Board(row_count=8, column_count=8, center_block=False)  

board.draw_board()

Round = 1
player1_ai = AI()
player2_ai = AI()

current_player = player1
current_ai = player1_ai
opponent = player2
opponent_ai = player2_ai

while True:
    actions = current_player.getValidActions(board)
    if not actions:
        # Skip turn if no valid moves
        print(f"Player {current_player.number} has no valid moves. Passing turn.")
    else:
        ai_action = current_ai.choose_action(board, current_player, opponent, depth)
        doAction(ai_action, current_player, board)
        print(
            f"AI {current_player.number} chose to place at "
            f"row={ai_action.row+1}, col={ai_action.col+1}"
        )

    board.draw_board()

    # Check if game over: both players have no moves or board is full
    player1_actions = player1.getValidActions(board)
    player2_actions = player2.getValidActions(board)
    if (not player1_actions and not player2_actions) or board.is_full():
        print(f"Round: {Round}\n")
        player1_count = board.count_pieces(player1)
        player2_count = board.count_pieces(player2)
        if player1_count > player2_count:
            print(f"{player1.number} wins with {player1_count} pieces!")
        elif player2_count > player1_count:
            print(f"{player2.number} wins with {player2_count} pieces!")
        else:
            print("Stalemate!")
        print(f"Player 1 pieces: {player1_count}")
        print(f"Player 2 pieces: {player2_count}")
        exit()

    # Switch players
    current_player, opponent = opponent, current_player
    current_ai, opponent_ai = opponent_ai, current_ai
    print(f"Round: {Round}\n")
    Round += 1