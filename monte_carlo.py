from ultimate_tic_tac_toe import *
import time

class MonteCarloNode:
    def __init__(self, board):
        self.actions = UltimateTicTacToe.actions(board)
        self.playouts = 0
        self.successors = [MonteCarloNode(UltimateTicTacToe.result(action, board)) for action in self.actions]

def select(tree):
    # TODO
    return tree
def expand(leaf):
    # TODO
    return
def simulate(node):
    # TODO
    return
def back_propagate(result):
    # TODO
    return
def monte_carlo_player(board, time_limit = 1):
    tree = MonteCarloNode(board)
    start = time.now()
    while time.now() - start < time_limit:
        leaf = select(tree)
        child = expand(leaf)
        result = simulate(child)
        back_propagate(result)
    best_action = None
    most_playouts = - float("inf")
    for i in range(len(tree.successors)):
        if (tree.successors[i].playouts >= most_playouts):
            most_playouts = tree.successors[i].playouts
            best_action = tree.actions[i]
    return best_action