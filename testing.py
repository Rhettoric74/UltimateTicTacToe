from minimax import *
from ultimate_tic_tac_toe import *
import json
if __name__ == "__main__":
    wins_dict = {"X": 0, "O": 0, "C": 0}
    dir_name = "results/monte_carlo_results"
    # enter the name of your test here, it should follow the format:
    # <descriptor of x-player agent>_vs_<descriptor of o-player agent>.json
    # for example:
    # random_agent_vs_heatmap_agent.json
    test_name = "winning_blocking_heatmap_playout_selection_ucb1_vs_heatmap_eval_d3_agent.json"
    # default sample size is 100
    for i in range(100):
        try:
            board = UltimateTicTacToeState()
            result = UltimateTicTacToe.play_game(board, monte_carlo_player, minimax_agent)
            wins_dict[result.winner] += 1
        except Exception as e:
            print(e)
            print("weird bug, missed a simulation")
    with open(dir_name + "/" + test_name, "w") as fw:
        json.dump(wins_dict, fw)
    print(wins_dict)