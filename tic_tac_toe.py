import copy
import random
class TicTacToeState:
    def __init__(self):
        self.grid = [["-" for i in range(3)] for j in range(3)]
        self.to_move = "X"
        self.winner = None
    def __repr__(self):
        string_board = ""
        for i in range(3):
            for j in range(3):
                string_board += self.grid[i][j] + " "
            string_board += "\n"
        if self.winner != None:
            string_board += str(self.winner) + " has won.\n"
        else:
            string_board += self.to_move + " to move.\n"
        return string_board

class TicTacToe:
    def __init__(self):
        self.initial = TicTacToeState()
    def is_terminal(state):
        for i in range(3):
            for char in ["X", "O"]:
                if state.grid[i][0] == char and char == state.grid[i][1] and char == state.grid[i][2]:
                    state.winner = char
                    return True
                if state.grid[0][i] == char and char == state.grid[1][i] and char == state.grid[2][i]:
                    state.winner = char
                    return True
        for char in ["X", "O"]:
            if state.grid[0][0] == char and char == state.grid[1][1] and char == state.grid[2][2]:
                state.winner = char
                return True 
            if state.grid[2][0] == char and char == state.grid[1][1] and char == state.grid[0][2]:
                state.winner = char
                return True 
        return False
    def actions(state):
        actions_list = []
        for i in range(3):
            for j in range(3):
                if state.grid[i][j] == "-":
                    actions_list.append([i, j])
        return actions_list
    def result(state, action):
        state_copy = copy.deepcopy(state)
        if state.grid[action[0]][action[1]] in "XO":
            raise(Exception("Attempted to move onto already occupied square"))
        state_copy.grid[action[0]][action[1]] = state.to_move
        if state.to_move == "X":
            state_copy.to_move = "O"
        if state.to_move == "O":
            state_copy.to_move = "X"
        if TicTacToe.is_terminal(state_copy):
            state_copy.winner = state.to_move
            state_copy.to_move = None
        elif TicTacToe.actions(state_copy) == []:
            state_copy.winner = "C"
            state_copy.to_move = None
        return state_copy
if __name__ == "__main__":
    board = TicTacToeState()
    while board.winner == None:
        print(board)
        action = random.choice(TicTacToe.actions(board))
        board = TicTacToe.result(board, action)
    print(board)
    
