from tic_tac_toe import TicTacToeState, TicTacToe

class UltimateTicTacToeState:
    def __init__(self):
        self.subboard_grid = [[TicTacToeState() for i in range(3)] for j in range(3)]
        self.to_move = "X"
        self.winner = None
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
                if state.grid[i][0] == char and char == state.grid[i][1] and char == state.grid[i][2]:
                    return True
        for char in ["X", "O"]:
            if state.grid[0][0] == char and char == state.grid[1][1] and char == state.grid[2][2]:
                return True 
            if state.grid[2][0] == char and char == state.grid[1][1] and char == state.grid[0][2]:
                return True 
        return False
if __name__ == "__main__":
    print(UltimateTicTacToeState())