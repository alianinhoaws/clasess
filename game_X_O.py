from random import randint


class Game:

    board = list(range(1, 10))
    game = None
    wins_combination = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]
    available_steps = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def __init__(self):
        self.player_choice = None
        self.compute_choice = None #  'X' if self.player_choice == 'O' else 'O'

    @classmethod
    def start_game(cls):
        while True:
            cls.game = input(f"Would you like to start the game \nY to start or N to exit: ")
            if cls.game not in ('YN'):
                print("Please use letters Y or N")
                continue
            if cls.game == 'N':
                return "Game exit"
            return

    def choice(self):
        while True:
            self.player_choice = input(f"Enter a choice X or O to start: ")
            if self.player_choice not in ('XO'):
                print("Please use letters X or O")
                continue
            if self.player_choice == 'X':
                self.compute_choice = '0'
            else:
                self.compute_choice = 'X'
            return self.player_choice, self.compute_choice

    def input(self):
        while True:
            value = input(f"Enter number of the field to set {self.player_choice}: ")
            try:
                value = int(value)
            except Exception as exc:
                print(f"Wrong choice: {exc}, \nPlease use number from 1 to 9")
                continue
            if value not in self.available_steps:
                print("Please use number from 1 to 9: ")
                continue
            if str(self.board[value-1]) in 'OX':
                print("Field is occupied")
                continue
            return value

    def step(self, value, player=None):
        if player:
            self.board[value - 1] = self.player_choice
        else:
            self.board[value - 1] = self.compute_choice
        return self.board

    def compute_step(self):
        board = self.board
        for combination in self.wins_combination:
            if (board[combination[0] - 1]) == (board[combination[1] - 1]) and \
                    self.player_choice in (board[combination[0] - 1]) and \
                    self.compute_choice not in (str(board[combination[2] - 1])):
                return board[combination[2] - 1]
            if (board[combination[0] - 1]) == (board[combination[2] - 1]) and \
                    self.player_choice in (board[combination[0] - 1]) and \
                    self.compute_choice not in (str(board[combination[1] - 1])):
                return board[combination[1] - 1]
            if (board[combination[1] - 1]) == (board[combination[2] - 1]) and \
                    self.player_choice in (board[combination[1] - 1]) and \
                    self.compute_choice not in (str(board[combination[0] - 1])):
                return board[combination[0] - 1]
        compute_step = randint(1, 9)
        while str(self.board[compute_step-1]) in 'XO':
            compute_step = randint(1, 9)
        return compute_step

    @staticmethod
    def draw_board():
        board = Game.board
        print('-------------')
        for x in range(3):
            print('|', board[0 + x * 3], '|', board[1 + x * 3], '|', board[2 + x * 3], '|')
        print('-------------')

    def check_if_win(self):
        board = self.board  # does it cast?
        if any(x in self.available_steps for x in board):
            for combination in self.wins_combination:
                if (board[combination[0]-1]) == (board[combination[1]-1]) == (board[combination[2]-1]):
                    return board[combination[1]-1]
        else:
            return "DRAW"
        return


if __name__ == '__main__':
    game = Game()
    win = game.start_game()
    if not win:
        player, computer = game.choice()
        if player == 'X':
            game.draw_board()
            value = game.input()
            game.step(value, player)
        game.draw_board()
        value = game.compute_step()
        game.step(value)
        game.draw_board()
    while not win:
       win = game.check_if_win()
       value = game.input()
       game.step(value, player)
       game.draw_board()
       win = game.check_if_win()
       value = game.compute_step()
       game.step(value)
       game.draw_board()
       win = game.check_if_win()
    print("Winner:", win)
