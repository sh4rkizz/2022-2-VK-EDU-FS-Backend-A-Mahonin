""" Module is being used to play a game of TIC-TAC-TOE """

from ai_player import AIPlayer


class TicTacGame:
    """ Player is able to choose type of game (PvP or PvE),
    PLayer plays the game by inputting digits from 1 to 9
    which are recounted as a coordinate tuple """

    def __init__(self):
        """ Creates starting board which is filled with '-' elements
        Also sets game settings and creates an AI if the player wants to play
        against a computer """

        self.table = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.prompt_board = [
            [len(self.table) * num_y + num_x + 1 for num_x in range(len(line))]
            for num_y, line in enumerate(self.table)
        ]

        self.player_tags = ['X', 'O']
        self.winner = None

        self.pve, self.player_tag = self.set_game_settings()

        self.active_ai = AIPlayer(
            tag=(set(self.player_tags) - set(self.player_tag)).pop(),
            player_tag=self.player_tag,
            field_size=len(self.table)
        ) if self.pve else None

        self.show_prompt_board()

    @staticmethod
    def set_game_settings() -> tuple[bool, str]:
        """ Sets game type (PvP/PvE) and player
        Sets preferred tag and AI strength for the PvE game (if it was picked) """

        game_mode = tag_choice = None
        allowed_tag_choice = ['X', 'x', 'х', 'Х', 'O', 'o', '0', 'о', 'О']

        while game_mode not in {'1', '2'}:
            game_mode = input('Choose game mode:\n\t1 - PvP\n\t2 - PvE\n\t').strip()

        if game_mode == '2':
            while tag_choice not in allowed_tag_choice:
                tag_choice = input('Choose the game symbol:\n\tX or O').strip()

            tag_choice = ['X', 'O'][not allowed_tag_choice.index(tag_choice) < 4]

        return bool(int(game_mode) - 1), tag_choice

    def show_prompt_board(self):
        """ Visualizes prompts for the input to play the game """

        for line in self.prompt_board:
            print(str(line).replace(',', ''))

    def show_board(self):
        """ Visualizes current playing board """

        print(*self.table, sep='\n')
        print('=' * 15)

    def validate(self, pos: str) -> (tuple[int, int], None):
        """ Interprets input as coordinates for the array

        returns coordinate tuple: if input is correct
        returns None: if input is incorrect or the cell is occupied"""

        allowed_positions = [str(x + 1) for x in range(len(self.table) ** 2)]

        if pos not in allowed_positions:
            if pos == '':
                print('You did not choose a position')
            elif not pos.isdigit():
                print('You need to use numeric position')
            else:
                print(f'You must use a number between {allowed_positions[0]} '
                      f'and {allowed_positions[-1]}')

            self.show_prompt_board()

            return None

        pos_y, pos_x = (int(pos) - 1) // 3, (int(pos) + 2) % 3

        if self.is_occupied(pos_y, pos_x):
            print('The cell you chose is already occupied by a player\n')

            return None

        return pos_y, pos_x

    def is_occupied(self, pos_y: int, pos_x: int) -> bool:
        """ Tells if the cell is occupied by a player """

        return self.table[pos_y][pos_x] != '-'

    def move(self, player_tag: str, ai_coordinate: tuple = None) -> (str, None):
        """ Simulates a player making a move,
        reserving a cell and checking its emptiness """

        while True:
            if ai_coordinate == -1 or self.winner is not None:
                return self.check_winner()

            if ai_coordinate is not None:
                pos_y, pos_x = ai_coordinate
            else:
                position = self.validate(input('Choose a cell you want to go for\n').strip())

                if position is None:
                    continue

                pos_y, pos_x = position

            self.table[pos_y][pos_x] = player_tag
            self.show_board()

            return self.check_winner()

    def is_draw(self) -> bool:
        """ Counts the number of empty cells
        returns true if all the cells are occupied """

        return [cell for line in self.table for cell in line].count('-') == 0

    def is_winning_line(self, line: list[tuple]) -> (str, bool):
        """ Counts line winning conditions """

        cells = [self.table[pos[0]][pos[1]] for pos in line]

        for tag in self.player_tags:
            if cells[0] == cells[1] == cells[2] == tag:
                self.winner = tag

                return tag

        return False

    def check_winner(self) -> (str, None):
        """ Provides winner control via sub indexing """

        if self.is_draw():
            self.winner = 'Friendship'

        lines_to_check = (
            # Diagonals
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],

            # Rows
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],

            # Columns
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
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
