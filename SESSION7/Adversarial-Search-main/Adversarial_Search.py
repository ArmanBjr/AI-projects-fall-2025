# Adversarial_Search.py
#4021262459
#4021262131
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
        beta = self.MAX_VALUE
        value, state = self.max(board, player, opponent, depth, alpha, beta)
        return state['action']

    def max(self, board: Board, player: Player, opponent: Player, depth, alpha, beta):
        # Todo
        if (player.terminal_test(board) and opponent.terminal_test(board)) or board.is_full() or depth == 0:
            return utility(board, player, opponent), None
        best_value = self.MIN_VALUE
        best_state = None
        successors = self.succesor(board, player, opponent)
        if not successors:
            return self.min(board, opponent, player, depth - 1, alpha, beta)
        for state in successors:
            nextB = state['board']
            nextP = state['player']    
            nextO = state['opponent'] 
            value, _ = self.min(nextB, nextP, nextO, depth - 1, alpha, beta)
            
            if value > best_value:
                best_value = value
                best_state = state
            if best_value >= beta:
                return best_value, best_state
            # if alpha >= beta:
            #     return best_value, best_state  
            if best_value > alpha:
                alpha = best_value      
        return best_value, best_state


    def min(self, board: Board, player: Player, opponent: Player, depth, alpha, beta):
        # Todo
        if (player.terminal_test(board) and opponent.terminal_test(board)) or board.is_full() or depth == 0:
            return utility(board, player, opponent), None
        worst_value = self.MAX_VALUE
        worst_state = None
        successors = self.succesor(board, player, opponent, reverse=True)
        if not successors:
            return self.max(board, opponent, player, depth - 1, alpha, beta)
        for state in successors:
            nextB = state['board']
            nextP = state['player']    
            nextO = state['opponent'] 
            value, _ = self.max(nextB, nextP, nextO, depth - 1, alpha, beta)
            if value < worst_value:
                worst_value = value
                worst_state = state
            if worst_value <= alpha:
                return worst_value, worst_state
            # if alpha >= beta:
            #     return worst_value, worst_state
            
            if worst_value < beta:
                beta = worst_value
        return worst_value, worst_state
