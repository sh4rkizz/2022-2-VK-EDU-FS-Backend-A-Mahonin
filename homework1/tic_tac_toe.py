""" Module is being used to play a game of TIC-TAC-TOE """

from numpy import arange, full, ndarray, diag, fliplr
from numpy import sum as np_sum

from ai_player import AIPlayer


class TicTacGame:
    """ Player is able to choose type of game (PvP or PvE),
    PLayer plays the game by inputting digits from 1 to 9
    which are recounted as a coordinate tuple """

    def __init__(self):
        """ Creates starting board (ndarray) which is filled with '-' elements
        Also sets game settings and creates an AI if the player wants to play
        against a computer """

        self.table = full((3, 3), '-')
        self.player_tags = ['X', 'O']
        self.winner = None

        self.pve, self.player_tag = self.set_game_settings()

        self.active_ai = AIPlayer(
            tag=(set(self.player_tags) - set(self.player_tag)).pop(),
            player_tag=self.player_tag,
        ) if self.pve else None

        self.show_prompt_board()

    @staticmethod
    def set_game_settings() -> tuple[bool, str]:
        """ Sets game type (PvP/PvE) and player
        Sets preferred tag and AI strength for the PvE game (if it was picked) """

        game_mode = tag_choice = None
        allowed_tag_choice = ['X', 'x', 'х', 'Х', 'O', 'o', '0', 'о', 'О']

        while game_mode not in {'1', '2'}:
            game_mode = input('Choose game mode:\n\t1 - PvP\n\t2 - PvE\n\t')

        if game_mode == '2':
            while tag_choice not in allowed_tag_choice:
                tag_choice = input('Choose the game symbol:\n\tX or O')

            tag_choice = ['X', 'O'][not allowed_tag_choice.index(tag_choice) < 4]

        return bool(int(game_mode) - 1), tag_choice

    @staticmethod
    def show_prompt_board():
        """ Visualizes prompts for the input to play the game """

        print(*arange(1, 10).reshape(3, 3), sep='\n')

    def show_board(self):
        """ Visualizes current playing board """

        print(*self.table, sep='\n')
        print('=' * 15)

    def validate(self, pos: str) -> (tuple[int, int], None):
        """ Interprets input as coordinates for the numpy.ndarray

        returns coordinate tuple: if input is correct
        returns None: if input is incorrect """

        allowed_positions = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

        try:
            if pos not in allowed_positions:
                raise ValueError

            pos = int(pos)
            return (pos - 1) // 3, (pos + 2) % 3
        except ValueError:
            print('You have to use given inputs to play the game')
            self.show_prompt_board()

            return None

    def is_occupied(self, coordinates: tuple) -> bool:
        """ Tells if the cell is occupied by a player """

        return self.table[coordinates] != '-'

    def move(self, player_tag: str, ai_coordinate: tuple = None) -> (str, None):
        """ Simulates a player making a move,
        reserving a cell and checking its emptiness """

        while True:
            if ai_coordinate == -1 or self.winner is not None:
                return self.check_winner()

            coordinates = ai_coordinate if ai_coordinate is not None else self.validate(input())

            if coordinates is not None:
                if not self.is_occupied(coordinates):
                    self.table[coordinates] = player_tag
                    self.show_board()

                    return self.check_winner()

                print('This cell is occupied')

    def is_draw(self) -> bool:
        """ Counts the number of empty cells
        returns true if all the cells are occupied """

        return np_sum(self.table.reshape(1, 9) == '-') == 0

    def is_winning_line(self, line: ndarray) -> (str, bool):
        """ Counts line winning conditions """

        for tag in self.player_tags:
            if np_sum(line == tag) == 3:
                self.winner = tag

                return tag

        return False

    def check_winner(self) -> (str, None):
        """ Provides winner control via sub indexing """

        if self.is_draw():
            self.winner = 'Friendship'

        lines_to_check = (
            diag(self.table),
            diag(fliplr(self.table)),
            self.table[0, :],
            self.table[1, :],
            self.table[2, :],
            self.table[:, 0],
            self.table[:, 1],
            self.table[:, 2],
        )

        for line in lines_to_check:
            if tag := self.is_winning_line(line):
                return tag

        return None

    def pvp_game(self, player=False):
        """ Simulates PvP game mode """

        while self.winner is None:
            print(f'Player {player + 1} move')

            self.move(self.player_tags[player])
            player = not player

        return self.winner

    def pve_game(self):
        """ Simulates PvE game mode """

        while self.winner is None:
            if self.player_tag == 'X':
                self.move(self.player_tag)
                self.move(
                    player_tag=self.active_ai.tag,
                    ai_coordinate=self.active_ai.analyze(self.table, lost=bool(self.winner))
                )
            else:
                self.move(
                    player_tag=self.active_ai.tag,
                    ai_coordinate=self.active_ai.analyze(self.table)
                )
                self.move(self.player_tag)

        return self.winner

    def start(self) -> None:
        """ Start a game of tic-tac-toe """

        self.show_board()
        print(f'{self.pvp_game() if self.active_ai is None else self.pve_game()} is a winner')


if __name__ == '__main__':
    game = TicTacGame()
    game.start()
