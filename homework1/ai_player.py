""" BOT-module to play TIC-TAC-TOE
Only very hard difficulty is available
Others are for noobs, which you are not """

from random import shuffle


class AIPlayer:
    """ Class AIPlayer represents a very tough to beat bot to play against
    It handles given board and returns a position tuple to make a move at """

    def __init__(self, tag: str, player_tag: str, field_size: int):
        self.player_tag = player_tag
        self.is_first_move = True
        self.field = None
        self.tag = tag

        self.iter_positions = [
            (pos_y, pos_x)
            for pos_y in range(field_size)
            for pos_x in range(field_size)
        ]

        self.lines_to_check = (
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

    def analyze(self, field: list = None, lost: bool = False) -> (int, tuple):
        """ Calculate moves with high priority
        attack and defense moves are being calculated separately """

        if lost or field is None or len(field) <= 0:
            return -1

        self.field = field

        return self.attack() if self.tag == 'X' else self.defense()

    def attack(self) -> tuple:
        """ Attack the human player, first move is pre-programmed """

        if self.is_first_move:
            self.is_first_move = False

            return 1, 1

        return self.choose_strategy()

    def find_traps(self) -> (tuple, None):
        """ Find a way to trap a player,
        making two or more X|-|X type lines """

        pos = None
        max_counter = 0

        # Sort through possible coordinates
        for pos_y, pos_x in self.iter_positions:
            count = 0

            if self.field[pos_y][pos_x] != '-':
                continue

            for line in self.lines_to_check:
                if (pos_y, pos_x) not in line:
                    continue

                cells = [self.field[pos[0]][pos[1]] for pos in line]

                if cells.count('X') == 1 and cells.count('O') == 0:
                    count += 1

            if count > max_counter:
                max_counter, pos = count, (pos_y, pos_x)

        return pos

    def defense(self) -> tuple:
        """ Defend positions, first move is pre-programmed """

        if self.is_first_move:
            self.is_first_move = False
            first_move_defence = {
                (0, 0): (1, 1), (0, 1): (0, 0), (0, 2): (1, 1),
                (1, 0): (2, 0), (1, 1): (0, 0), (1, 2): (0, 2),
                (2, 0): (1, 1), (2, 1): (2, 0), (2, 2): (1, 1)
            }

            for pos_y, pos_x in self.iter_positions:
                if self.field[pos_y][pos_x] == self.player_tag:
                    return first_move_defence[pos_y, pos_x]

        return self.choose_strategy()

    def choose_strategy(self) -> tuple:
        """ Method for choice of game strategy """

        pos = self.search_for_win_or_lose(find_win=True)
        pos = pos if pos is not None else self.search_for_win_or_lose(find_win=False)
        pos = pos if pos is not None else self.find_traps()

        return pos if pos is not None else self.make_simple_move()

    def search_for_win_or_lose(self, find_win: bool = False) -> (tuple, None):
        """ Check for X|X|-, X|-|X, -|X|X or
        O|O|-, -|O|O, O|-|O lines to defend or to win the game """

        tags = (
            self.player_tag,
            self.tag
        )

        for pos_y, pos_x in self.iter_positions:
            if self.field[pos_y][pos_x] != '-':
                continue

            for line in self.lines_to_check:
                if (pos_y, pos_x) not in line:
                    continue

                cells = [self.field[pos[0]][pos[1]] for pos in line]

                if cells.count(tags[find_win]) == 2 and cells.count(tags[not find_win]) == 0:
                    for ret_y, ret_x in line:
                        if self.field[ret_y][ret_x] != tags[find_win]:
                            return ret_y, ret_x

        return None

    def make_simple_move(self) -> tuple:
        """ 'If nothing is working
        just pretend you are completely random'
        returns random position which is 100% up for grabs """

        to_shuffle = [
            (pos_y, pos_x)
            for (pos_y, pos_x) in self.iter_positions
            if self.field[pos_y][pos_x] == '-'
        ]

        shuffle(to_shuffle)

        return to_shuffle[0]
