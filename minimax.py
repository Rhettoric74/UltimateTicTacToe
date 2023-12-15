# minimax.py
import random
import json
from ultimate_tic_tac_toe import UltimateTicTacToe, UltimateTicTacToeState, random_agent, heatmap_agent, user_input_agent
from monte_carlo import *

# Updated MinimaxNode class
class MinimaxNode:
    def __init__(self, board):
        self.board = board
        self.actions = UltimateTicTacToe.actions(board)
        self.children = []

    def expand(self):
        if self.board.winner == None and self.children == []:
            self.children = [MinimaxNode(UltimateTicTacToe.result(self.board, action)) for action in self.actions]

# Updated minimax function
def minimax(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or UltimateTicTacToe.is_terminal(state):
        return evaluate(state)

    if maximizing_player:
        max_eval = float('-inf')
        for action in UltimateTicTacToe.actions(state):
            child_state = UltimateTicTacToe.result(state, action)
            eval = minimax(child_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for action in UltimateTicTacToe.actions(state):
            child_state = UltimateTicTacToe.result(state, action)
            eval = minimax(child_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Updated minimax_agent function
def minimax_agent(board):
    root = MinimaxNode(board)
    root.expand()

    best_value = float('-inf')
    best_action = None
    alpha = float('-inf')
    beta = float('inf')

    for child in root.children:
        value = minimax(child.board, depth=3, alpha=alpha, beta=beta, maximizing_player=False)
        if value > best_value:
            best_value = value
            best_action = root.actions[root.children.index(child)]
    return best_action


def evaluate(state):
    # Use the heatmap function as the evaluation function
    if state.to_move == "X":
        return sum(sum(row) for row in state.x_heatmap)
    elif state.to_move == "O":
        return sum(sum(row) for row in state.o_heatmap)
    else:
        if state.winner == "X":
            return 25
        elif state.winner == "O":
            return -25
        else:
            return 0



if __name__ == "__main__":
    wins_dict = {"X": 0, "O": 0, "C": 0}
    dir_name = "results/minimax_results"
    # enter the name of your test here, it should follow the format:
    # <descriptor of x-player agent>_vs_<descriptor of o-player agent>.json
    # for example:
    # random_agent_vs_heatmap_agent.json
    test_name = "heatmap_eval_d3_agent_vs_winning_blocking_heatmap_agent.json"
    # default sample size is 100
    for i in range(100):
        try:
            board = UltimateTicTacToeState()
            #mc = MonteCarloAgent(board)
            result = UltimateTicTacToe.play_game(board, minimax_agent, winning_blocking_heatmap_agent)
            wins_dict[result.winner] += 1
        except:
            print("weird bug, missed a simulation")
    with open(dir_name + "/" + test_name, "w") as fw:
        json.dump(wins_dict, fw)
    print(wins_dict)
