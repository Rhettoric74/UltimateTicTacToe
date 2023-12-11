from ultimate_tic_tac_toe import *
import math
import time
import copy
import json
class MinimaxNode:
    def __init__(self, board):
        self.board = board
        self.actions = UltimateTicTacToe.actions(board)
        self.successors = []


def minimax_expand(node):
    if node.board.winner is None and not node.successors:
        for action in node.actions:
            # add all successors to the successors list
            node.successors.append(MinimaxNode(UltimateTicTacToe.result(node.board, action)))


def minimax_simulate(node, target_winner):
    simulation_path = [node]
    cur_node = node
    while cur_node.board.winner is None and cur_node.actions:
        minimax_expand(cur_node)
        # use the minimax selection policy here
        cur_node = minimax_select(cur_node)
        simulation_path.append(cur_node)

    if cur_node.board.winner == target_winner:
        return 1, simulation_path
    if cur_node.board.winner == "C":
        return 0.5, simulation_path
    return 0, simulation_path


def minimax_select(node):
    # implement the minimax selection policy here
    best_score, best_action = minimax_search(node, node.board.to_move)
    return node.successors[node.actions.index(best_action)] if best_action is not None else None


def minimax_search(node, target_winner, alpha=-float('inf'), beta=float('inf')):
    if node.board.winner is not None or not node.actions:
        return eval_fn(node.board), None  # Terminal state, return the utility

    best_action = None
    if node.board.to_move == target_winner:  # MAX player
        best_score = -float('inf')
        for successor in node.successors:
            score, _ = minimax_search(successor, target_winner, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = successor.actions[0]  # Assumes actions list is non-empty
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cutoff
    else:  # MIN player
        best_score = float('inf')
        for successor in node.successors:
            score, _ = minimax_search(successor, target_winner, alpha, beta)
            if score < best_score:
                best_score = score
                best_action = successor.actions[0]  # Assumes actions list is non-empty
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cutoff

    return best_score, best_action


def eval_fn(state):
    # Implement a simple evaluation function for the given state
    # You can customize this function based on your preferences
    return state.utility(state, state.to_move)


def minimax_player(board):
    print("Minimax algorithm called")
    tree = MinimaxNode(board)
    minimax_expand(tree)
    target_winner = board.to_move

    # Call the minimax_search function with appropriate parameters
    result = minimax_search(tree, target_winner)
    
    best_action = result[1] if result else None
    print("Best score:", result[0])
    return best_action


if __name__ == "__main__":
    wins_dict = {"X": 0, "O": 0, "C": 0}
    for i in range(100):
        board = UltimateTicTacToeState()
        result = UltimateTicTacToe.play_game(board, minimax_player, random_agent)
        wins_dict[result.winner] += 1
    print(wins_dict)
    policy = "minimax_with_alpha_beta_pruning"
    with open("results/" + policy + ".json", "w") as fw:
        json.dump(wins_dict, fw)


# from game.py from book
'''
def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


'''