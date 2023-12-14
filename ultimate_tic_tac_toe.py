from tic_tac_toe import TicTacToeState, TicTacToe
import copy
import random
import json

class UltimateTicTacToeState:
    def __init__(self):
        self.subboard_grid = [[TicTacToeState() for i in range(3)] for j in range(3)]
        self.x_heatmap = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]
        self.o_heatmap = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]
        self.to_move = "X"
        self.winner = None
        self.last_move = None
    def __repr__(self):
        outstring = ""
        for row in range(3):
            for subboard_row in range(3):
                for col in range(3):
                    for subboard_col in range(3):
                        outstring += self.subboard_grid[row][col].grid[subboard_row][subboard_col] + " "
                    if col != 2:
                        outstring += "# "
                outstring += "\n"
            if row != 2:
                outstring += "#####################\n"
        if self.winner != None:
            outstring += self.winner + " has won."
        else:
            outstring += self.to_move + " to move."
        return outstring
    def update_heatmaps(self):
        winners_grid = []
        for i in range(3):
            winners_grid.append([])
            for j in range(3):
                winners_grid[i].append(self.subboard_grid[i][j].winner)
        for i in range(3):
            for j in range(3):
                o_wins_possible = 0
                if "X" not in winners_grid[i]:
                    o_wins_possible += 1
                if "X" not in [row[j] for row in winners_grid]:
                    o_wins_possible += 1
                # add to diagonal heatmaps if they are possible
                if (i == j) and "X" not in [winners_grid[k][k] for k in range(3)]:
                    o_wins_possible += 1
                if (i == 2 - j) and "X" not in [winners_grid[k][2 - k] for k in range(3)]:
                    o_wins_possible += 1
                self.o_heatmap[i][j] = o_wins_possible
                x_wins_possible = 0
                if "O" not in winners_grid[i]:
                    x_wins_possible += 1
                if "O" not in [row[j] for row in winners_grid]:
                    x_wins_possible += 1
                # add to diagonal heatmaps if they are possible
                if (i == j) and "O" not in [winners_grid[k][k] for k in range(3)]:
                    x_wins_possible += 1
                if (i == 2 - j) and "O" not in [winners_grid[k][2 - k] for k in range(3)]:
                    x_wins_possible += 1
                self.x_heatmap[i][j] = x_wins_possible
    
class UltimateTicTacToe:
    def __init__(self):
        self.initial = UltimateTicTacToeState()
    def is_terminal(state):
        for i in range(3):
            for char in ["X", "O"]:
                if state.subboard_grid[i][0].winner == char and char == state.subboard_grid[i][1].winner and char == state.subboard_grid[i][2].winner:
                    return True
                if state.subboard_grid[0][i].winner == char and char == state.subboard_grid[1][i].winner and char == state.subboard_grid[2][i].winner:
                    return True
        for char in ["X", "O"]:
            if (state.subboard_grid[0][0].winner == char) and (char == state.subboard_grid[1][1].winner) and (char == state.subboard_grid[2][2].winner):
                return True 
            if state.subboard_grid[2][0].winner == char and char == state.subboard_grid[1][1].winner and char == state.subboard_grid[0][2].winner:
                return True 
        return False
    def actions(state):
        if state.last_move != None:
            if state.subboard_grid[state.last_move[2]][state.last_move[3]].winner == None:
                subboard_actions = TicTacToe.actions(state.subboard_grid[state.last_move[2]][state.last_move[3]])
                return [(state.last_move[2], state.last_move[3], action[0], action[1]) for action in subboard_actions]            
        return [(i, j, k, l) for i in range(3) for j in range(3) for k in range(3) for l in range(3) if (state.subboard_grid[i][j].winner == None and state.subboard_grid[i][j].grid[k][l] == "-")]
    def result(state, action):
        i, j, k, l = action
        if state.subboard_grid[i][j].grid[k][l] != "-" or state.subboard_grid[i][j].winner != None:
            raise(Exception("Attempted to move onto occupied space"))
        state_copy = copy.deepcopy(state)
        state.subboard_grid[i][j].to_move = state.to_move
        state_copy.subboard_grid[i][j] = TicTacToe.result(state.subboard_grid[i][j], (k, l))
        if state.to_move == "X":
            state_copy.to_move = "O"
        if state.to_move == "O":
            state_copy.to_move = "X"
        if UltimateTicTacToe.is_terminal(state_copy):
            state_copy.winner = state.to_move
            state_copy.to_move = None
        elif UltimateTicTacToe.actions(state_copy) == []:
            state_copy.winner = "C"
            state_copy.to_move = None
        state_copy.last_move = action
        state_copy.update_heatmaps()
        return state_copy
    def play_game(board, x_player, o_player, quiet = False):
        turn_counter = 0
        while board.winner == None:
            actions = UltimateTicTacToe.actions(board)
            if (len(actions) > 9) and not quiet:
                print("any subboard available to move")
            if turn_counter % 2 == 0:
                board = UltimateTicTacToe.result(board, x_player(board))
            else:
                board = UltimateTicTacToe.result(board, o_player(board))
            if not quiet:
                print(board)
                #print(board.x_heatmap)
                #print(board.o_heatmap)
            turn_counter += 1
        return board
def heatmap_agent(board):
    best_heatmap_value = 0
    best_action = None
    actions = UltimateTicTacToe.actions(board)
    for i in range(len(actions)):
        if board.to_move == "O":
            board_heatmap_val = UltimateTicTacToe.result(board, actions[i]).o_heatmap[actions[i][0]][actions[i][1]]
            subboard_heatmap_val = UltimateTicTacToe.result(board, actions[i]).subboard_grid[actions[i][0]][actions[i][1]].o_heatmap[actions[i][2]][actions[i][3]]
        elif board.to_move == "X":
            board_heatmap_val = UltimateTicTacToe.result(board, actions[i]).x_heatmap[actions[i][0]][actions[i][1]]
            subboard_heatmap_val = UltimateTicTacToe.result(board, actions[i]).subboard_grid[actions[i][0]][actions[i][1]].x_heatmap[actions[i][2]][actions[i][3]]
        if board_heatmap_val + subboard_heatmap_val >= best_heatmap_value:
            best_heatmap_value = board_heatmap_val + subboard_heatmap_val
            best_action = actions[i]
    return best_action
def random_agent(board):
    return random.choice(UltimateTicTacToe.actions(board))
def user_input_agent(board):
    actions_list = [str(action).strip(" ") for action in UltimateTicTacToe.actions(board)]
    print("Actions available:", actions_list)
    action = input("Choose an action from the list")
    while action.strip(" ") not in actions_list:
        action = input("Action not available, choose again from the list")
    return tuple(map(int, action[1:-1].split(",")))

            

if __name__ == "__main__":
    wins_dict = {"X": 0, "O": 0, "C": 0}
    dir_name = "results/simple_heuristic_results"
    # enter the name of your test here, it should follow the format:
    # <descriptor of x-player agent>_vs_<descriptor of o-player agent>.json
    # for example:
    # random_agent_vs_heatmap_agent.json
    test_name = "random_agent_vs_heatmap_agent.json"
    # default sample size is 100
    for i in range(100):
        try:
            board = UltimateTicTacToeState()
            result = UltimateTicTacToe.play_game(board, random_agent, heatmap_agent)
            wins_dict[result.winner] += 1
        except:
            print("weird bug, missed a simulation")
    with open(dir_name + "/" +  test_name, "w") as fw:
        json.dump(wins_dict, fw)
    print(wins_dict)

