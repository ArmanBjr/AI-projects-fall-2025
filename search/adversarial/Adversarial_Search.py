# Adversarial_Search.py

import copy
from player import Player
from Board import Board
from Action import doAction
from utility import *


class AI:
    MIN_VALUE = -1000000
    MAX_VALUE = 1000000

    def choose_action(self, board, player, opponent, max_depth):
        best_action = self.do_minimax(
            copy.deepcopy(board),
            copy.copy(player),
            copy.copy(opponent),
            max_depth,
        )
        return best_action

    def deepCopy(self, player, opponent, board) -> tuple[Player, Player, Board]:
        player_copy = copy.deepcopy(player)
        opponent_copy = copy.deepcopy(opponent)
        next_board = copy.deepcopy(board)
        return player_copy, opponent_copy, next_board

    def succesor(self, board: Board, player: Player, opponent: Player, reverse=False):
        if (reverse):
            actions = opponent.getValidActions(board)
        else:
            actions = player.getValidActions(board)

        result = []
        for action in actions:
            player_copy, opponent_copy, next_board = self.deepCopy(player, opponent, board)

            if (reverse):
                doAction(action, opponent_copy, next_board)
            else:
                doAction(action, player_copy, next_board)

            result.append({'board': next_board, 'player': player_copy, 'opponent': opponent_copy, 'action': action})

        return result

    def do_minimax(self, board: Board, player: Player, opponent: Player, depth: int):
        # Todo
        # Add alpha beta
        alpha = self.MIN_VALUE
        beta  = self.MAX_VALUE
        value, state = self.max(board, player, opponent, depth, alpha, beta)
        return state['action']

    # def max(self, board: Board, player: Player, opponent: Player, depth):
    #     # Todo
    #     pass


    # def min(self, board: Board, player: Player, opponent: Player, depth):
    #     # Todo
    #     pass

    def max(self, board: Board, player: Player, opponent: Player, depth: int, alpha: int, beta: int):
        """
        MAX node: it's `player`'s turn.
        We want the move that maximizes utility(board, player, opponent).
        Returns (best_value, best_state_dict).
        """

        # Check cutoff or no-move
        player_moves   = player.getValidActions(board)
        opponent_moves = opponent.getValidActions(board)

        game_over_now = (
            depth == 0 or
            board.is_full() or
            (len(player_moves) == 0 and len(opponent_moves) == 0)
        )

        if game_over_now:
            return utility(board, player, opponent), None

        # If player cannot move but opponent can, in Othello we "pass":
        # here we don't just stop; we let MIN move without changing the board.
        if len(player_moves) == 0 and len(opponent_moves) > 0:
            # pass the turn -> MIN's turn with same board
            return self.min(board, opponent, player, depth - 1, alpha, beta)

        best_value = self.MIN_VALUE
        best_state = None

        successors = self.succesor(board, player, opponent)

        for state in successors:
            next_board    = state['board']
            next_player   = state['player']     # this was the mover
            next_opponent = state['opponent']   # this was the other guy

            # After player moves, it's opponent's turn -> MIN
            value, _ = self.min(next_board, next_opponent, next_player,
                                depth - 1, alpha, beta)

            if value > best_value:
                best_value = value
                best_state = state

            # alpha-beta update
            if best_value > alpha:
                alpha = best_value
            if alpha >= beta:
                break  # prune

        return best_value, best_state

    def min(self, board: Board, player: Player, opponent: Player, depth: int, alpha: int, beta: int):
        """
        MIN node: it's `player`'s turn (this "player" is the opponent of the MAX from above).
        We want to minimize MAX's score.
        Ultimately, evaluation must still be from opponent's opponent = original MAX pov.
        """

        player_moves   = player.getValidActions(board)
        opponent_moves = opponent.getValidActions(board)

        game_over_now = (
            depth == 0 or
            board.is_full() or
            (len(player_moves) == 0 and len(opponent_moves) == 0)
        )

        if game_over_now:
            # IMPORTANT:
            # Here `player` is the minimizing player (the opponent of MAX),
            # and `opponent` is MAX.
            # utility(board, max_player, min_player)
            return utility(board, opponent, player), None

        # Handle "pass" turn if MIN-player has no legal moves
        if len(player_moves) == 0 and len(opponent_moves) > 0:
            # pass back to MAX without changing board
            return self.max(board, opponent, player, depth - 1, alpha, beta)

        worst_value = self.MAX_VALUE
        worst_state = None

        successors = self.succesor(board, player, opponent)

        for state in successors:
            next_board    = state['board']
            next_player   = state['player']     # mover at this step
            next_opponent = state['opponent']   # the other one

            # After MIN moves, it's MAX's turn again
            value, _ = self.max(next_board, next_opponent, next_player,
                                depth - 1, alpha, beta)

            if value < worst_value:
                worst_value = value
                worst_state = state

            # alpha-beta update
            if worst_value < beta:
                beta = worst_value
            if beta <= alpha:
                break  # prune

        return worst_value, worst_state