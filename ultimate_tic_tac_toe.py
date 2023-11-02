from tic_tac_toe import TicTacToeState, TicTacToe
import copy
import random

class UltimateTicTacToeState:
    def __init__(self):
        self.subboard_grid = [[TicTacToeState() for i in range(3)] for j in range(3)]
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
            if state.subboard_grid[0][0].winner == char and char == state.subboard_grid[1][1].winner and char == state.subboard_grid[2][2].winner:
                return True 
            if state.subboard_grid[2][0].winner == char and char == state.subboard_grid[1][1].winner and char == state.subboard_grid[0][2].winner:
                return True 
        return False
    def actions(state):
        if state.last_move != None:
            if state.subboard_grid[state.last_move[2]][state.last_move[3]].winner == None:
                subboard_actions = TicTacToe.actions(state.subboard_grid[state.last_move[0]][state.last_move[1]])
                return [(state.last_move[0], state.last_move[1], action[0], action[1]) for action in subboard_actions]
            
        return [(i, j, k, l) for i in range(3) for j in range(3) for k in range(3) for l in range(3) if (state.subboard_grid[i][j].winner == None and state.subboard_grid[i][j].grid[k][l] == "-")]
    def result(state, action):
        i, j, k, l = action
        if state.subboard_grid[i][j].grid[k][l] != "-" or state.subboard_grid[i][j].winner != None:
            raise(Exception("Attempted to move onto occupied space"))
        state_copy = copy.deepcopy(state)
        state_copy.subboard_grid[i][j].grid[k][l] = state.to_move
        if state.to_move == "X":
            state_copy.to_move = "O"
        if state.to_move == "O":
            state_copy.to_move = "X"
        if TicTacToe.is_terminal(state_copy.subboard_grid[i][j]):
            state_copy.winner = state.to_move
            state_copy.to_move = None
        elif TicTacToe.actions(state_copy.subboard_grid[i][j]) == []:
            state_copy.winner = "C"
            state_copy.to_move = None
        if UltimateTicTacToe.is_terminal(state_copy):
            state_copy.winner = state.to_move
            state_copy.to_move = None
        elif UltimateTicTacToe.actions(state_copy) == []:
            state_copy.winner = "C"
            state_copy.to_move = None
        return state_copy
            

if __name__ == "__main__":
    board = UltimateTicTacToeState()
    print(board)
    while board.winner == None:
        actions = UltimateTicTacToe.actions(board)
        if (len(actions) > 9):
            print("any subboard available to move")
        board = UltimateTicTacToe.result(board, random.choice(actions))
        print(board)
