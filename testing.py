from minimax import *
from ultimate_tic_tac_toe import *
import json
if __name__ == "__main__":
    wins_dict = {"X": 0, "O": 0, "C": 0}
    dir_name = "results/minimax_results"
    # enter the name of your test here, it should follow the format:
    # <descriptor of x-player agent>_vs_<descriptor of o-player agent>.json
    # for example:
    # random_agent_vs_heatmap_agent.json
    test_name = "heatmap_eval_d5_agent_vs_winning_blocking_heatmap_playout_selection_ucb1.json"
    # default sample size is 100
    for i in range(100):
        board = UltimateTicTacToeState()
        mc = MonteCarloAgent()
        result = UltimateTicTacToe.play_game(board, minimax_agent, mc.move)
        wins_dict[result.winner] += 1
    with open(dir_name + "/" + test_name, "w") as fw:
        json.dump(wins_dict, fw)
    print(wins_dict)