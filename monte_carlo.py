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
        self.states_to_successors_dict = {}
    def __repr__(self):
        board = str(self.board)
        return board + "\nWins: " + str(self.wins) + "\nPlayouts" + str(self.playouts)
    def expand(node):
        if node.board.winner == None and node.successors == []:
            for action in node.actions:
                # add all successors to the successors list
                successor_state = UltimateTicTacToe.result(node.board, action)
                successor_node = MonteCarloNode(successor_state)
                node.successors.append(successor_node)
                node.states_to_successors_dict[str(successor_state)] = successor_node

    def random_policy(node):
        return random.choice(node.successors)
    def heatmap_policy(node):
        best_heatmap_value = 0
        best_successor = None
        for i in range(len(node.actions)):
            if node.board.to_move == "O":
                board_heatmap_val = node.successors[i].board.o_heatmap[node.actions[i][0]][node.actions[i][1]]
                subboard_heatmap_val = node.successors[i].board.subboard_grid[node.actions[i][0]][node.actions[i][1]].o_heatmap[node.actions[i][2]][node.actions[i][3]]
            elif node.board.to_move == "X":
                board_heatmap_val = node.successors[i].board.x_heatmap[node.actions[i][0]][node.actions[i][1]]
                subboard_heatmap_val = node.successors[i].board.subboard_grid[node.actions[i][0]][node.actions[i][1]].x_heatmap[node.actions[i][2]][node.actions[i][3]]
            if board_heatmap_val + subboard_heatmap_val >= best_heatmap_value:
                best_heatmap_value = board_heatmap_val + subboard_heatmap_val
                best_successor = node.successors[i]
        return best_successor
    def winning_blocking_heatmap_policy(node):
        # check if you can win a subboard or block a subboard from the state.
        # always win the subboard if you can
        # always block the subboard if you can but you can't win
        best_heatmap_value = 0
        best_successor = None
        for i in range(len(node.actions)):
            if UltimateTicTacToe.result(node.board, node.actions[i]).subboard_grid[node.actions[i][0]][node.actions[i][1]].winner in ["X", "O"]:
                return node.successors[i]
        # block any actions that would result in an opponent win
        opponent_board = copy.deepcopy(node.board)
        if node.board.to_move == "X":
            opponent_board.to_move = "O"
        else:
            opponent_board.to_move = "X"
        for i in range(len(node.actions)):
            if UltimateTicTacToe.result(opponent_board, node.actions[i]).subboard_grid[node.actions[i][0]][node.actions[i][1]].winner in ["X", "O"]:
                return node.successors[i]
        for i in range(len(node.actions)):
            if node.board.to_move == "O":
                board_heatmap_val = node.successors[i].board.o_heatmap[node.actions[i][0]][node.actions[i][1]]
                subboard_heatmap_val = node.successors[i].board.subboard_grid[node.actions[i][0]][node.actions[i][1]].o_heatmap[node.actions[i][2]][node.actions[i][3]]
            elif node.board.to_move == "X":
                board_heatmap_val = node.successors[i].board.x_heatmap[node.actions[i][0]][node.actions[i][1]]
                subboard_heatmap_val = node.successors[i].board.subboard_grid[node.actions[i][0]][node.actions[i][1]].x_heatmap[node.actions[i][2]][node.actions[i][3]]
            if board_heatmap_val + subboard_heatmap_val >= best_heatmap_value:
                best_heatmap_value = board_heatmap_val + subboard_heatmap_val
                best_successor = node.successors[i]
        return best_successor
            
    def simulate(node, target_winner, playout_policy = winning_blocking_heatmap_policy):
        simulation_path = [node]
        cur_node = node
        while cur_node.board.winner == None and cur_node.actions != []:
            ''' print("Cur board")
            print(cur_node.board) '''
            MonteCarloNode.expand(cur_node)
            cur_node = playout_policy(cur_node)
            ''' print("updated board")
            print(cur_node.board) '''
            simulation_path.append(cur_node)
        if cur_node.board.winner == target_winner:
            return 1, simulation_path
        if cur_node.board.winner == "C":
            return 0.5, simulation_path
        return 0, simulation_path
    def win_rate_over_log_playouts(successor, simulations):
        if successor.playouts == 0:
            score = 1
        else:
            score = (successor.wins / successor.playouts) / math.log(successor.playouts + 2)
        return score
    def ucb_one(successor, simulations, c = math.sqrt(2)):
        if successor.playouts == 0:
            return 1
        else:
            return successor.wins / successor.playouts + c * math.sqrt(math.log(simulations) / successor.playouts)
    def select(tree, simulations, selection_score = ucb_one):
        # TODO: try different policies for this
        # current policy: score nodes based on their win percentage divided by the natural log of the number of playouts plus 2
        # pick the node with the highest score
        best_score = 0
        best_node = None
        for successor in tree.successors:
            score = selection_score(successor, simulations)
            if score >= best_score:
                best_score = score
                best_node = successor
        return best_node
    def back_propagate(node, result, target_winner):
        added_wins, simulation_path = result
        node.wins += added_wins
        node.playouts += 1
        for visited_node in simulation_path:
            if visited_node.board.to_move == target_winner:
                visited_node.wins += added_wins
                #print(visited_node.wins)
            visited_node.playouts += 1

def monte_carlo_search(tree, time_limit = 1):
    print("Monte carlo tree search called")
    MonteCarloNode.expand(tree)
    target_winner = tree.board.to_move
    start = time.time()
    simulations = 0
    while time.time() - start < time_limit:
        simulations += 1
        leaf = MonteCarloNode.select(tree, simulations)
        MonteCarloNode.expand(leaf)
        result = MonteCarloNode.simulate(leaf, target_winner)
        MonteCarloNode.back_propagate(leaf, result, target_winner)
    print("simulations run:", simulations)
    best_action = None
    best_node = None
    best_win_rate = - float("inf")
    for i in range(len(tree.successors)):
        if tree.successors[i].playouts == 0:
            win_rate = 0
        else:
            win_rate = tree.successors[i].wins / tree.successors[i].playouts
        if (win_rate >= best_win_rate):
            best_win_rate = win_rate
            best_action = tree.actions[i]
            best_node = tree.successors[i]
    print(best_win_rate)
    return best_action, best_node
class MonteCarloAgent:
    def __init__(self, board = UltimateTicTacToeState()):
        self.root = MonteCarloNode(board)
        self.cur_node = self.root
    def move(self, state):
        # get the node that your opponent played on from last time
        MonteCarloNode.expand(self.cur_node)
        opponents_node = self.root
        if str(state) in self.cur_node.states_to_successors_dict:
            opponents_node = self.cur_node.states_to_successors_dict[str(state)]
        action, node = monte_carlo_search(opponents_node)
        self.cur_node = node
        print(node.playouts)
        return action




if __name__ == "__main__":
    wins_dict = {"X": 0, "O": 0, "C": 0}
    dir_name = "results/monte_carlo_results"
    # enter the name of your test here, it should follow the format:
    # <descriptor of x-player agent>_vs_<descriptor of o-player agent>.json
    # for example:
    # random_agent_vs_heatmap_agent.json
    test_name = "winning_blocking_heatmap_playout_selection_ucb1_vs_heatmap_agent.json"
    # default sample size is 100
    for i in range(100):
        try:
            board = UltimateTicTacToeState()
            mc = MonteCarloAgent()
            result = UltimateTicTacToe.play_game(board, mc.move, heatmap_agent)
            wins_dict[result.winner] += 1
        except Exception as e:
            print(e)
            print("weird bug, missed a simulation")
    with open(dir_name + "/" + test_name, "w") as fw:
        json.dump(wins_dict, fw)
    print(wins_dict)
        