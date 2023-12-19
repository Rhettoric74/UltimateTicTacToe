# minimax.py
import random
import json
from ultimate_tic_tac_toe import UltimateTicTacToe, UltimateTicTacToeState, random_agent, heatmap_agent, user_input_agent
from monte_carlo import *
who_turn = None
# Updated MinimaxNode class
class MinimaxNode:
    def __init__(self, board, function):
        self.board = board
        self.actions = UltimateTicTacToe.actions(board)
        self.children = []
        self.function = function

    def expand(self):
        if self.board.winner == None and self.children == []:
            self.children = [MinimaxNode(UltimateTicTacToe.result(self.board, action), self.function) for action in self.actions]

# Updated minimax function
    def minimax(self, state, depth, alpha, beta, maximizing_player):
        
        if depth == 0 or UltimateTicTacToe.is_terminal(state):
            x = self.function(state) #change this for different state evaluations 
            if who_turn == "X":
                return x
            else:
                return -x
            
            

        if maximizing_player:
            max_eval = float('-inf')
            for action in UltimateTicTacToe.actions(state):
                child_state = UltimateTicTacToe.result(state, action)
                eval = self.minimax(child_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for action in UltimateTicTacToe.actions(state):
                child_state = UltimateTicTacToe.result(state, action)
                eval = self.minimax(child_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

# Updated minimax_agent function
def minimax_agent(board):
    global who_turn
    who_turn = board.to_move
    if who_turn == "X":
        root = MinimaxNode(board, function = evaluate1)
    else:
        root = MinimaxNode(board, function = evaluate_game)
    root.expand()
    best_value = float('-inf')
    best_action = None
    alpha = float('-inf')
    beta = float('inf')
    
    for child in root.children:
        value = root.minimax( child.board, depth=3, alpha=alpha, beta=beta, maximizing_player=True)
        if value > best_value:
            best_value = value
            best_action = root.actions[root.children.index(child)]
    return best_action


def evaluate_game(state):
    position = state.subboard_grid
    evale = 0
    main_bd = []
    evaluator_mul = [[1.4, 1, 1.4],[1, 1.75, 1], [1.4, 1, 1.4]]
    # this is weight based on which sub game is more important 

    if state.winner == "X":
        evale += 5000
    elif state.winner == "O":
        evale -= 5000
    #if the X or O is the winner 

    #for through all sub games
    for eh in range(3):
        for ah in range(3):
            evale += evaluate_sub_game(position[eh][ah]) * 1.5 * evaluator_mul[eh][ah]
    
            #checking winners for sub games 
            tmp_ev = 0 
            if position[eh][ah].winner == "X":
                tmp_ev = 1
            elif position[eh][ah].winner == "O":
                tmp = -1
            main_bd.append(tmp_ev)

    #evaluating the entire board, but inputting as a sub board of win, draws, or losses 
    evale += evaluate_sub_game(main_bd) * 150

    return evale

def evaluate_sub_game(state):
    evaluation = 0
    points = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]
    pos = []
    symbol_mapping = {'X': 1, '-': 0, 'O': -1}
    
    
    if (type(state) != list):
        for rows in state.grid:
            for i in rows:
                pos.append(symbol_mapping[i])
    else:
        pos = state
    for bw in range(len(pos)):
        evaluation += pos[bw] * points[bw]

    #looking for two in the rows, of the opponet 
    if pos[0] + pos[1] + pos[2] == -2 or pos[3] + pos[4] + pos[5] == -2 or pos[6] + pos[7] + pos[8] == -2:
        evaluation -= 6
    
    if pos[0] + pos[3] + pos[6] == -2 or pos[1] + pos[4] + pos[7] == -2 or pos[2] + pos[5] + pos[8] == -2:
        evaluation -= 6
     
    if pos[0] + pos[4] + pos[8] == -2 or pos[2] + pos[4] + pos[6] == -2:
        evaluation -= 7



   # looking for two in a rows for the minimax agent 
    if pos[0] + pos[1] + pos[2] == 2 or pos[3] + pos[4] + pos[5] == 2 or pos[6] + pos[7] + pos[8] == 2:
        evaluation += 6
    if pos[0] + pos[3] + pos[6] == 2 or pos[1] + pos[4] + pos[7] == 2 or pos[2] + pos[5] + pos[8] == 2:
        evaluation += 6
    if pos[0] + pos[4] + pos[8] == 2 or pos[2] + pos[4] + pos[6] == 2:
        evaluation += 7


    if (type(state) != list):
        if state.winner == "X":
            evaluation += 12
        elif state.winner == "O":
            evaluation -= 12
    return evaluation


def evaluate1(state):
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
    for i in range(10):
        board = UltimateTicTacToeState()
        o_agent =  minimax_agent
        x_agent = minimax_agent
        result = UltimateTicTacToe.play_game(board,   x_agent, o_agent)
        wins_dict[result.winner] += 1
  
    print(wins_dict)
   