import random

wins_combination = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]
available_steps = (1, 2, 3, 4, 5, 6, 7, 8, 9)


class GameIterator:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def __iter__(self):
        self.player_move = True
        return self

    def __next__(self):
        if self.player_move:
            self.player_move = False
            return self.player1
        else:
            self.player_move = True
            return self.player2


class Game:

    board_size_w = 3
    board_size_s = 10

    def __init__(self):
        self.board = list(range(1, self.board_size_s))

    def __call__(self):
        while True:
            game = input(f"Would you like to start the game \nY to start or N to exit: ")
            if game not in ('YN'):
                print("Please use letters Y or N")
                continue
            if game == 'N':
                return "Game exit"
            else:  # can be added multiplayer mood
                self.reset_board()
                choice = self.choice_func()
                player = Player(choice, self.board)
                computer = Computer(choice, self.board)
                print(self.gaming(player, computer))

    def reset_board(self):
        self.board = list(range(1, self.board_size_s))

    def gaming(self, player, computer):
        game = GameIterator(player, computer)
        for step, player in enumerate(game):
            player()
            self.draw_board()
            self.check_if_win()
            if step == 8:
                break

    def draw_board(self):
        # ASCI Draw
        board = self.board
        size = self.board_size_w
        print(13*'-')
        for x in range(size):
            print('|',
                  board[0 + x * size], '|', board[1 + x * size], '|', board[2 + x * size],
                  '|')  # if more than 2 - make loop
        print(13*'-')

    def choice_func(self):
        choices = {
            "X": ("X", "O"),
            "O": ("O", "X")
        }
        while True:
            self.choice = input("Enter a choice X or O to start: ")
            # if self.player_choice not in choices.keys(): # if we have 2 options if else, if we have more than 2 dict.
            #     print("Please use letters X or O")
            #     continue
            # self.player_choice, self.compute_choice = choices.get(self.player_choice)
            if self.choice not in 'XO':  # if we have 2 options if else, if we have more than 2 dict.
                print("Please use letters X or O")
                continue
            return self.choice

    def check_if_win(self):
        board = self.board   # need to repair if draw
        if any(x in available_steps for x in board):
            for combination in wins_combination:
                if (board[combination[0]-1]) == (board[combination[1]-1]) == (board[combination[2]-1]):
                    return board[combination[1]-1]
                else:
                    return
        return 'DRAW'


class Player(Game):

    def __init__(self, choice, board):
        self.choice = choice
        super().__init__()
        self.board = board

    def __call__(self):
        while True:
            value = input(f"Enter number of the field to set {self.choice}: ")
            try:
                value = int(value)
            except Exception as exc:
                print(f"Wrong choice: {exc}, \nPlease use number from 1 to 9")
                continue
            if value not in available_steps:
                print("Please use number from 1 to 9: ")
                continue
            if str(self.board[value-1]) in 'OX':
                print("Field is occupied")
                continue
            return self.step(value, self.choice)

    def step(self, value, choice):
        self.board[value - 1] = choice
        return self.board


class Computer(Player):

    def __init__(self, choice, board):
        self.choice = choice
        self.compute_choice = 'X' if choice == 'O' else 'O'
        super().__init__(choice, board)
        self.board = board

    def __call__(self):
        player_choice = self.choice
        potential_moves = list(filter(lambda item: isinstance(item, int), self.board))
        # filter ints from the board to
        # determine what steps are available ('O', 'X' are ignored)
        compute_step = random.choice(potential_moves)  # from the list of numbers make random choice
        for move in potential_moves:  # Iterate list of ints ready to step
            board = self.board[:]  # make a copy of board to make next step of player virtual
            next_move = move - 1  # make next move from iterated ints from the board (variable "move")
            # -1 because board is a list (stats from 0)
            # Make this virtual move of the player to the board
            board[next_move] = player_choice  # add X or O (player's character)
            player_pos = list(filter(lambda item: item != 0,
                                [index + 1 if v == player_choice else 0
                                 for index, v in enumerate(board)]))  # iterate board result =>
            # is positions where players 'X' already stayed + virtual move
            # NEXT BLOCK check if this move can give a win for a player
            if len(player_pos) >= len(wins_combination[0]):  # check if players 'X' with 1 virtual are 3 or more
                # (2 is not enough to finish a line)
                # to enter the cycle to determine if this step can give winning combination
                for combination in wins_combination:
                    if set(combination).issubset(player_pos):  # check if e-x: in combination #1 1,2,3
                        # is all numbers of player position (list of all players 'X' + virtual 1)
                        compute_step = move  # compute step will be virtual move if combination is matched
                        break
        return self.step(compute_step, self.compute_choice)


if __name__ == '__main__':  # all should be in Game() objects players/computer/board separate
    game = Game()
    game()
