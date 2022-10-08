""" Module to test TIC-TAC-TOE bot """

import unittest
from unittest.mock import patch

from numpy import array, full

from tic_tac_toe import TicTacGame


class BaseMoveCase(unittest.TestCase):
    """ Class for unified setUp process """

    @patch('builtins.input', side_effect=['2', 'X'])
    def setUp(self, mock_game_mode) -> None:
        self.Game = TicTacGame()
        self.Game.table = array(
            [['-', 'X', 'X'],
             ['-', 'O', 'O'],
             ['X', 'O', '-']]
        )

        self.Game.active_ai.analyze(self.Game.table)
        self.Game.active_ai.is_first_move = False


class TestGameCreation(unittest.TestCase):
    @patch('builtins.input', side_effect=['2', 'X'])
    def test_create_game_x(self, mock_game_mode):
        self.Game = TicTacGame()

        self.assertEqual(self.Game.table.size, 9)
        self.assertEqual(self.Game.player_tag, 'X')

    @patch('builtins.input', side_effect=['2', 'O'])
    def test_create_game_o(self, mock_game_mode):
        self.Game = TicTacGame()

        self.assertEqual(self.Game.table.size, 9)
        self.assertEqual(self.Game.player_tag, 'O')

    @patch('builtins.input', side_effect=['1221', '2', 'abc', 'x'])
    def test_negative_game_creation(self, mock_game_mode):
        self.Game = TicTacGame()

        self.assertEqual(self.Game.table.size, 9)
        self.assertEqual(self.Game.player_tag, 'X')
        self.assertEqual(self.Game.active_ai.tag, 'O')

    @patch('builtins.input', side_effect=['2', 'O'])
    def test_empty_field(self, mock_input):
        self.Game = TicTacGame()

        self.assertRaises(ValueError, self.Game.active_ai.analyze, None)
        self.assertRaises(ValueError, self.Game.active_ai.analyze, array([]))


class TestGameplayDefense(BaseMoveCase):
    def test_first_move_defense(self):
        self.Game.active_ai.is_first_move = True
        self.Game.table = array([['X', '-', '-'], ['-', '-', '-'], ['-', '-', '-']])

        self.assertIsNotNone(self.Game.table)
        self.assertEqual(self.Game.active_ai.analyze(self.Game.table), (1, 1))

    def test_plain_defense(self):
        self.Game.table = array([['X', '-', 'X'], ['O', '-', '-'], ['-', '-', '-']])

        self.assertEqual(self.Game.active_ai.analyze(self.Game.table), (0, 1))

    def test_main_diagonal_defense(self):
        self.Game.table = array([['X', '-', '-'], ['O', 'X', '-'], ['-', '-', '-']])
        self.assertEqual(self.Game.active_ai.analyze(self.Game.table), (2, 2))

    def test_secondary_diagonal_defense(self):
        self.Game.table = array([['-', '-', 'X'], ['O', 'X', '-'], ['-', '-', '-']])
        self.assertEqual(self.Game.active_ai.analyze(self.Game.table), (2, 0))

    def test_simple_move(self):
        self.assertIsNotNone(self.Game.active_ai.make_simple_move())

    def test_lost(self):
        self.Game.winner = 'X'

        self.assertEqual(self.Game.active_ai.analyze(self.Game.table, self.Game.winner), -1)

    def test_find_enemy_traps(self):
        self.Game.table = array([['-', '-', 'X'], ['-', 'X', '-'], ['O', '-', '-']])
        self.assertEqual(self.Game.active_ai.try_to_trap(enemy_traps=True), (0, 0))


class TestGameplayAttack(BaseMoveCase):
    @patch('builtins.input')
    def setUp(self, mock_game_mode) -> None:
        super().setUp()

        self.Game.active_ai.tag = 'X'
        self.Game.player_tag = self.Game.active_ai.player_tag = 'O'

    def test_win_position(self):
        self.assertEqual(self.Game.active_ai.attack(), (0, 0))

    def test_first_move_attack(self):
        self.Game.active_ai.is_first_move = True
        self.Game.table = full((3, 3), '-')

        self.assertEqual(self.Game.active_ai.tag, 'X')
        self.assertEqual(self.Game.active_ai.attack(), (1, 1))

    def test_defense_in_attack(self):
        self.Game.table = array([['X', '-', '-'], ['-', 'X', '-'], ['-', 'O', 'O']])

        self.assertEqual(self.Game.active_ai.analyze(self.Game.table), (2, 0))

    def test_try_to_trap(self):
        self.Game.table = array([['-', '-', 'X'], ['-', 'X', 'O'], ['O', '-', '-']])
        self.assertEqual(self.Game.active_ai.try_to_trap(), (0, 0))


if __name__ == '__main__':
    unittest.main()
