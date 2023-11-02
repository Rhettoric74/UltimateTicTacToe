import copy

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
            string_board += str(self.winner) + "has won.\n"
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
    def result(state, player, action):
        state_copy = copy.deepcopy(state)
        if state.grid[action[0]][action[1]] not in "XO":
            raise(Exception("Attempted to move onto already occupied square"))
        state_copy.grid[action[0]][action[1]] = player
        if player == "X":
            state_copy.to_move = "O"
        if player == "O":
            state_copy.to_move = "X"
        return state_copy
if __name__ == "__main__":
    print(TicTacToeState())
