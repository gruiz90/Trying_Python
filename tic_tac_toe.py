"""
Tic Tac Toe game
"""
#from IPython.display import clear_output


def display_board(board):
    """
    Displays current playing board
    """
    display_board_str = ""
    # top_slice, mid_slice and low_slice in that order
    board_slices = [board[7:], board[4:7], board[1:4]]
    counter = 0
    for board_slice in board_slices:
        display_board_str += "     |     |     \n"
        display_board_str += create_line(board_slice)
        display_board_str += "     |     |     \n"
        if counter < 2:
            display_board_str += "- - - - - - - - -\n"
        counter += 1
    print(display_board_str)


def create_line(board_slice):
    """
    Creates a line of the board and return it
    """
    line_str = ""
    for item in board_slice:
        if item == "X":
            line_str += "  X  |"
        elif item == "O":
            line_str += "  O  |"
        else:
            line_str += "     |"
    return line_str[:-1] + "\n"


def check_win_condition(board, win_conditions_available):
    """
    Checks if the current board has a winning condition
    """
    win = False
    win_conditions = []
    for win_condition in win_conditions_available:
        x_1 = board[win_condition[0]]
        x_2 = board[win_condition[1]]
        x_3 = board[win_condition[2]]
        remove_win_condition = False
        if x_1 != "" and x_2 != "" and x_3 != "":
            if x_1 == x_2 == x_3:
                win = True
                break
            else:
                # This win condition is no longer available, so I remove it from the list
                remove_win_condition = True
        elif x_1 == "" and x_2 != "" and x_3 != "":
            if x_2 != x_3:
                remove_win_condition = True
        elif x_2 == "" and x_1 != "" and x_3 != "":
            if x_1 != x_3:
                remove_win_condition = True
        elif x_3 == "" and x_1 != "" and x_2 != "":
            if x_1 != x_2:
                remove_win_condition = True
        if not remove_win_condition:
            win_conditions.append(win_condition)
    return (win, win_conditions)


def tic_tac_toe():
    """
    Main function to execute tic tac toe game
    """
    print("Welcome to Tic Tac Toe!")
    player1_symbol = ""
    while True:
        player1_symbol = input("Player 1: Do you want to be X or O?\n").upper()
        if (player1_symbol != "X" and player1_symbol != "O"):
            print('Invalid input!')
        else:
            break
    players_symbols = ["#", player1_symbol]
    if player1_symbol == "X":
        players_symbols.append("O")
    else:
        players_symbols.append("X")
    win_conditions_init = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                           [1, 4, 7], [2, 5, 8], [3, 6, 9],
                           [1, 5, 9], [3, 5, 7]]
    win_conditions_available = win_conditions_init.copy()
    board_init = ['#', '', '', '', '', '', '', '', '', '']
    board = board_init.copy()
    positions_init = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    available_positions = positions_init.copy()
    current_player = 1
    keep_playing = True

    while keep_playing:
        print('\n'*100)
        # clear_output()
        display_board(board)
        position = 0
        while True:
            position = int(input(f"Player{current_player}({players_symbols[current_player]}): \
                                   Choose your next position from the set: \
                                   {available_positions}\n"))
            if position not in available_positions:
                print(f"Invalid input! Must be a number belonging to the set: \
                        {available_positions}")
            else:
                break
        available_positions.remove(position)
        board[position] = players_symbols[current_player]

        state = check_win_condition(board, win_conditions_available)
        win = state[0]
        win_conditions_available = state[1]
        if win or not win_conditions_available:
            print('\n'*100)
            # clear_output()
            display_board(board)
            if win:
                print(f"Congratulations Player {current_player}\
                        ({players_symbols[current_player]})! \
                        You have won the game!")
            else:
                # It's a tie
                print("No more winning conditions available. It's a tie!")

            while True:
                again = input(
                    "Do you want to play again? Enter Yes or No:\n").upper()
                if again != "YES" and again != "NO":
                    print('Invalid input! Valid inputs are Yes or No...')
                else:
                    if again == "NO":
                        keep_playing = False
                    break
            if not keep_playing:
                break
            # Here I need to reset everything
            current_player = 1
            board = board_init.copy()
            win_conditions_available = win_conditions_init.copy()
            available_positions = positions_init.copy()
        else:
            current_player += 1
            if current_player == 3:
                current_player = 1


# Execute tic_tac_toe()
tic_tac_toe()
