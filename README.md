# UltimateTicTacToe
Final project for CSCI4511W, Intro AI, in which we implement and evaluate various algorithms for their performance as agents in the game of Ultimate Tic Tac Toe.
Group members: Rhett Olson (olso9295@umn.edu), Nicholas Normandin-Parker (norma484@umn.edu)

# How to Play Against our Models:
1. Edit the testing.py script's main function to specify the agent you want to play against.
- Options include mc.move (for a monte carlo model), minimax_agent (for a MiniMax algorithm model), and the heuristic agents winning_blocking_heatmap_agent, stochastic_heatmap_agent, heatmap_agent, and random_agent.
- Passing in the agent "user_input_agent" will allow you to manually enter actions, put it first to play manually as the X player and second to play as the O player.
2. Set hyperparameters for the model you are using.
- If you are using monte_carlo search, edit the default parameter in the "simulate()" function to use the playout policy of your choice. Currently implemented options are random_policy, heatmap_policy, and winning_blocking_heatmap_policy.
- If you are using minimax_agent, set the depth limit inside of the call to minimax() inside of the minimax_agent() function of minimax.py. Higher depths will take longer to run, but depth limits of 3-5 find actions within a few seconds.
3. Run the script testing.py using the terminal command "python3 testing.py"
4. user_input agents will be given a list of actions in the format (i, j, k, l), and will need to enter an action from that list.
- the number i gives the index 0-2 of which row of the subboard grid the agent will play in.
- the number j gives the index 0-2 of which column of the subboard grid the agent will play in.
- the number k gives the index 0-2 of which row within the subboard agent will play in.
- the number j gives the index 0-2 of which column within the subboard the agent will play in.
- example: (2, 2, 1, 1) would represent playing in the bottom left subboard, in the middle square within that board.
- Always enter spaces after each comma to exactly match the format (i, j, k, l).