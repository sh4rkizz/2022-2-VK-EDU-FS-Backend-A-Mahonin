""" Module to test TIC-TAC-TOE game """

import unittest
from unittest.mock import patch

from tic_tac_toe import TicTacGame


class BaseCase(unittest.TestCase):
    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def setUp(self, mock_game_mode, mock_print) -> None:
        self.Game = TicTacGame()


class TestCreateGamePvP(unittest.TestCase):
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', '4', '2', '3', '1', '5', '6', '8', '7', '9'])
    def test_start_game(self, mock_game, mock_print):
        self.Game = TicTacGame()
        self.assertIsNotNone(self.Game)
        self.assertIsNone(self.Game.start())  # If it did not fail: the game is finished
        self.assertEqual(self.Game.winner, 'Friendship')

    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def test_set_game_settings(self, mock_input, mock_print):
        self.Game = TicTacGame()

        self.assertEqual(len(self.Game.table) ** 2, 9)
        self.assertIsNone(self.Game.active_ai)
        self.assertFalse(self.Game.pve)


class TestValidation(BaseCase):
    @patch('builtins.print')
    def test_validate(self, mock_print):
        self.assertEqual(self.Game.validate('1'), (0, 0))
        self.assertEqual(self.Game.validate('9'), (2, 2))

    @patch('builtins.print')
    def test_negative_validate(self, mock_print):
        self.assertIsNone(self.Game.validate('13'))


class TestLineHandling(BaseCase):
    @patch('builtins.print')
    @patch('builtins.input', return_value='1')
    def setUp(self, mock_input, mock_print) -> None:
        super().setUp()
        self.Game.table = [
            ['O', '-', 'X'],
            ['X', 'X', 'X'],
            ['O', 'O', '-']
        ]

    def test_is_occupied(self):
        self.assertTrue(self.Game.is_occupied(0, 0))
        self.assertFalse(self.Game.is_occupied(0, 1))

    def test_is_winning_line(self):
        self.assertEqual(self.Game.is_winning_line([(1, 0), (1, 1), (1, 2)]), 'X')

    def test_negative_is_winning_line(self):
        self.assertFalse(self.Game.is_winning_line([(0, 0), (0, 1), (0, 2)]))

    def test_is_draw(self):
        self.Game.table = [
            ['O', 'X', 'O'],
            ['X', 'O', 'X'],
            ['X', 'O', 'X']
        ]

        self.assertTrue(self.Game.is_draw())

    def test_check_winner(self):
        self.assertEqual(self.Game.check_winner(), 'X')

    def test_negative_check_winner(self):
        self.Game.table = [
            ['O', 'X', 'O'],
            ['X', 'O', 'X'],
            ['X', 'O', 'X']
        ]

        self.assertIsNone(self.Game.check_winner())


class TestGameOn(unittest.TestCase):
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', '4', '2', '3', '1', '5', '6', '8', '7', '9'])
    def test_pvp_game(self, mock_input, mock_print):
        self.Game = TicTacGame()
        self.Game.pvp_game()

        self.assertEqual(self.Game.winner, 'Friendship')


class TestGameplayPvE(BaseCase):
    @patch('builtins.print')
    @patch('builtins.input', return_value='5')
    def test_move_empty(self, mock_input, mock_print):
        self.assertIsNone(self.Game.move('X'))

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['13', '3'])
    def test_negative_out_move(self, mock_input, mock_print):
        self.assertIsNone(self.Game.move('X'))
        self.assertEqual(self.Game.table[0][2], 'X')

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6', '7'])
    def test_play_entire_game(self, mock_input, mock_print):
        self.Game.start()

        self.assertEqual(self.Game.winner, 'X')

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['4', '2', '3', '1', '5', '6', '8', '7', '9'])
    def test_play_till_the_draw(self, mock_input, mock_print):
        self.Game.start()

        self.assertEqual(self.Game.winner, 'Friendship')

    @patch('builtins.print')
    @patch('builtins.input', return_value='5')
    def test_winning_series_move(self, mock_input, mock_print):
        self.Game.table = [
            ['O', '-', 'X'],
            ['-', '-', '-'],
            ['X', 'O', '-']
        ]

        self.assertEqual(self.Game.move('X'), 'X')


if __name__ == '__main__':
    unittest.main()
