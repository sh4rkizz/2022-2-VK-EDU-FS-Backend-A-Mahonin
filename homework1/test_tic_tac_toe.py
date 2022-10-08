""" Module to test TIC-TAC-TOE game """

import unittest
from unittest.mock import patch

from numpy import array

from tic_tac_toe import TicTacGame


class BaseCase(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    def setUp(self, mock_game_mode) -> None:
        self.Game = TicTacGame()


class TestCreateGamePvP(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '4', '2', '3', '1', '5', '6', '8', '7', '9'])
    def test_start_game(self, mock_game):
        self.Game = TicTacGame()
        self.assertIsNotNone(self.Game)
        self.assertIsNone(self.Game.start())  # If it did not fail that means that the game is finished
        self.assertEqual(self.Game.winner, 'Friendship')

    @patch('builtins.input', return_value='1')
    def test_set_game_settings(self, mock_input):
        self.Game = TicTacGame()

        self.assertEqual(self.Game.table.size, 9)
        self.assertIsNone(self.Game.active_ai)
        self.assertFalse(self.Game.pve)


class TestValidation(BaseCase):
    def test_validate(self):
        self.assertEqual(self.Game.validate('1'), (0, 0))
        self.assertEqual(self.Game.validate('9'), (2, 2))

    @patch('builtins.input', side_effect=['a', '5'])
    def test_negative_validate(self, mock_input):
        self.assertIsNone(self.Game.validate(input()))
        self.assertEqual(self.Game.validate(input()), (1, 1))


class TestLineHandling(BaseCase):
    @patch('builtins.input', return_value='1')
    def setUp(self, mock_input) -> None:
        super().setUp()
        self.Game.table = array(
            [['O', '-', 'X'],
             ['X', 'X', 'X'],
             ['O', 'O', '-']]
        )

    def test_is_occupied(self):
        self.assertTrue(self.Game.is_occupied((0, 0)))
        self.assertFalse(self.Game.is_occupied((0, 1)))

    def test_is_winning_line(self):
        self.assertEqual(self.Game.is_winning_line(self.Game.table[1, :]), 'X')

    def test_negative_is_winning_line(self):
        self.assertFalse(self.Game.is_winning_line(self.Game.table[0, :]))

    def test_is_draw(self):
        self.Game.table = array(
            [['O', 'X', 'O'],
             ['X', 'O', 'X'],
             ['X', 'O', 'X']]
        )

        self.assertTrue(self.Game.is_draw())

    def test_check_winner(self):
        self.assertEqual(self.Game.check_winner(), 'X')

    def test_negative_check_winner(self):
        self.Game.table = array(
            [['O', 'X', 'O'],
             ['X', 'O', 'X'],
             ['X', 'O', 'X']]
        )

        self.assertIsNone(self.Game.check_winner())


class TestGameOn(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '4', '2', '3', '1', '5', '6', '8', '7', '9'])
    def test_pvp_game(self, mock_input):
        self.Game = TicTacGame()
        self.Game.pvp_game()

        self.assertEqual(self.Game.winner, 'Friendship')

    @patch('builtins.input', side_effect=['2', 'X', '5', '3', '4', '2', '9'])
    def test_pve_game_x(self, mock_input):
        self.Game = TicTacGame()

        self.Game.pve_game()
        self.assertEqual(self.Game.winner, 'Friendship')

    @patch('builtins.input', side_effect=['2', 'O', '1', '8', '3', '4'])
    def test_pve_game_o(self, mock_input):
        self.Game = TicTacGame()

        self.Game.pve_game()
        self.assertEqual(self.Game.winner, 'Friendship')


class TestGameplayPvE(BaseCase):
    @patch('builtins.input', return_value='5')
    def test_move_empty(self, mock_input):
        self.assertIsNone(self.Game.move('X'))

    @patch('builtins.input', side_effect=['13', '3'])
    def test_negative_out_move(self, mock_input):
        self.assertIsNone(self.Game.move('X'))
        self.assertEqual(self.Game.table[(0, 2)], 'X')

    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6', '7'])
    def test_play_entire_game(self, mock_input):
        self.Game.start()

        self.assertEqual(self.Game.winner, 'X')

    @patch('builtins.input', side_effect=['4', '2', '3', '1', '5', '6', '8', '7', '9'])
    def test_play_till_the_draw(self, mock_input):
        self.Game.start()

        self.assertEqual(self.Game.winner, 'Friendship')

    @patch('builtins.input', return_value='5')
    def test_winning_series_move(self, mock_input):
        self.Game.table = array(
            [['O', '-', 'X'],
             ['-', '-', '-'],
             ['X', 'O', '-']]
        )

        self.assertEqual(self.Game.move('X'), 'X')


if __name__ == '__main__':
    unittest.main()
