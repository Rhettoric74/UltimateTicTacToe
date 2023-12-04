from ultimate_tic_tac_toe import *
import math
import time
import copy
import json
class MonteCarloNode:
    def __init__(self, board):
        self.board = board
        self.actions = UltimateTicTacToe.actions(board)
        self.playouts = 0
        self.wins = 0
        self.successors = []
    def expand(node):
        if node.successors == []:
            for action in node.actions:
                node.successors.append(MonteCarloNode(UltimateTicTacToe.result(board, action)))
    def simulate(node, target_winner = "X", playout_policy = random_agent):
        simulated_game = UltimateTicTacToe.play_game(copy.deepcopy(node.board), playout_policy, playout_policy, True)
        if simulated_game.winner == target_winner:
            return 1
        return 0
    def select(tree):
        # TODO: try different policies for this
        # current policy: score nodes based on their win percentage divided by the natural log of the number of playouts plus 2
        # pick the node with the highest score
        best_score = 0
        best_node = None
        for successor in tree.successors:
            if successor.playouts == 0:
                score = 1
            else:
                score = (successor.wins / successor.playouts) / math.log(successor.playouts + 2)
            if score >= best_score:
                best_score = score
                best_node = successor
        return best_node
    def back_propagate(node, result):
        node.wins += result
        node.playouts += 1
def monte_carlo_player(board, time_limit = 1):
    print("Monte carlo tree search called")
    tree = MonteCarloNode(board)
    MonteCarloNode.expand(tree)
    target_winner = board.to_move
    start = time.time()
    simulations = 0
    while time.time() - start < time_limit:
        simulations += 1
        leaf = MonteCarloNode.select(tree)
        MonteCarloNode.expand(leaf)
        result = MonteCarloNode.simulate(leaf, target_winner)
        MonteCarloNode.back_propagate(leaf, result)
    print("simulations run:", simulations)
    best_action = None
    best_win_rate = - float("inf")
    for i in range(len(tree.successors)):
        if tree.successors[i].playouts == 0:
            win_rate = 0
        else:
            win_rate = tree.successors[i].wins / tree.successors[i].playouts
        if (win_rate >= best_win_rate):
            best_win_rate = win_rate
            best_action = tree.actions[i]
    return best_action
if __name__ == "__main__":
    wins_dict = {"X":0, "O":0, "C":0}
    for i in range(100):
        board = UltimateTicTacToeState()
        result = UltimateTicTacToe.play_game(board, monte_carlo_player, random_agent)
        wins_dict[result.winner] += 1
    print(wins_dict)
    with open("results.json", "w") as fw:
        json.dump(wins_dict, fw)
        