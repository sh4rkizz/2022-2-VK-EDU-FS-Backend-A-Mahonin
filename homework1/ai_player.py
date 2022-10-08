""" BOT-module to play TIC-TAC-TOE
Only very hard difficulty is available
Others are for noobs, which you are not """

from random import shuffle

from numpy import ndarray, copy, where
from numpy import sum as np_sum


class AIPlayer:
    """ Class AIPlayer represents a very tough to beat bot to play against
    It handles given board and returns a position tuple to make a move at

    Line numbering looks like this:
    diag0  5   6   7
          -------------
       2  |   |   |   |
          -------------
       3  |   |   |   |
          -------------
       4  |   |   |   |
          -------------
    diag1
    """

    def __init__(self, tag: str, player_tag: str):
        self.field = self.stack_field = self.lines_to_check = self.line_positions = None
        self.player_tag = player_tag
        self.is_first_move = True
        self.tag = tag

    def analyze(self, field: ndarray = None, lost: bool = False) -> (int, tuple):
        """ Calculate moves with high priority
        attack and defense moves are being calculated separately """

        if lost:
            return -1

        if field is not None and field.size > 0:
            self.field = field
            self.stack_field = copy(field)

            self.lines_to_check = (
                self.stack_field[[0, 1, 2], [0, 1, 2]],
                self.stack_field[[2, 1, 0], [0, 1, 2]],
                self.stack_field[0, :],
                self.stack_field[1, :],
                self.stack_field[2, :],
                self.stack_field[:, 0],
                self.stack_field[:, 1],
                self.stack_field[:, 2]
            )

            self.line_positions = {
                (0, 0): [0, 2, 5],
                (0, 1): [2, 6],
                (0, 2): [1, 2, 7],
                (1, 0): [3, 5],
                (1, 1): [0, 1, 3, 6],
                (1, 2): [3, 7],
                (2, 0): [1, 4, 5],
                (2, 1): [4, 6],
                (2, 2): [0, 4, 7]
            }

            return self.attack() if self.tag == 'X' else self.defense()

        raise ValueError

    def attack(self) -> tuple:
        """ Attack the human player, first move is pre-programmed """

        if self.is_first_move:
            self.is_first_move = False

            return 1, 1

        return self.choose_strategy()

    def try_to_trap(self, enemy_traps=False) -> (tuple, None):
        """ Find a way to trap a player,
        making two or more X|-|X type lines """

        trap_tags = (
            self.player_tag,
            self.tag
        )

        pos = None
        max_counter = 0

        for buff_pos, lines in self.line_positions.items():
            count = 0

            if self.field[buff_pos] != '-':
                continue

            for line in lines:
                if np_sum(self.lines_to_check[line] == trap_tags[enemy_traps]) == 1 and \
                        np_sum(self.lines_to_check[line] == trap_tags[not enemy_traps]) == 0:
                    count += 1

            if count > max_counter:
                max_counter, pos = count, buff_pos

        return pos

    def defense(self) -> tuple:
        """ Defend positions, first move is pre-programmed """

        if self.is_first_move:
            self.is_first_move = False
            first_move_defence = {
                (0, 0): (1, 1),
                (0, 1): (0, 0),
                (0, 2): (1, 1),
                (1, 0): (2, 0),
                (1, 1): (0, 0),
                (1, 2): (0, 2),
                (2, 0): (1, 1),
                (2, 1): (2, 0),
                (2, 2): (1, 1)
            }

            return first_move_defence[tuple(elem[0] for elem in where(self.field == 'X'))]

        return self.choose_strategy()

    def choose_strategy(self) -> tuple:
        """ Method for choice of game strategy """

        pos = self.search_for_win_or_lose(find_win=True)
        pos = pos if pos is not None else self.search_for_win_or_lose(find_win=False)
        pos = pos if pos is not None else self.try_to_trap()

        return pos if pos is not None else self.make_simple_move()

    def search_for_win_or_lose(self, find_win: bool = False) -> (tuple, None):
        """ Check for X|X|-, X|-|X, -|X|X or
        O|O|-, -|O|O, O|-|O lines to defend or to win the game """

        check_tag = (
            self.player_tag,
            self.tag
        )

        for enum, line in enumerate(self.lines_to_check):
            if np_sum(line == check_tag[find_win]) == 2 \
                    and np_sum(line == check_tag[not find_win]) == 0:

                if enum == 0:
                    self.stack_field[[0, 1, 2], [0, 1, 2]] = where(line != '-', line, self.tag)
                elif enum == 1:
                    self.stack_field[[2, 1, 0], [0, 1, 2]] = where(line != '-', line, self.tag)
                else:
                    line[int(where(line == '-')[0])] = self.tag

                return tuple(elem[0] for elem in where(self.field != self.stack_field))

        return None

    def make_simple_move(self) -> tuple:
        """ 'If nothing is working
        just pretend you are completely random'
        returns random position which is 100% up for grabs """

        to_shuffle = [x for x in self.line_positions if self.field[x] == '-']
        shuffle(to_shuffle)

        return to_shuffle[0]
