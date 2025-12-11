import unittest
import sys
from unittest.mock import patch
from assistant.cli import main

class TestCLI(unittest.TestCase):
    @patch('assistant.cli.schedule_reminder')
    def test_remind_command(self, mock_schedule):
        with patch('sys.argv', ['cli.py', 'remind', 'Test message', '--time', '10:00']):
            main()
            mock_schedule.assert_called_with('Test message', '10:00')

    @patch('assistant.cli.add_note')
    def test_note_add_command(self, mock_add):
        with patch('sys.argv', ['cli.py', 'note', 'add', 'Test note']):
            main()
            mock_add.assert_called_with('Test note')

    @patch('assistant.cli.list_notes')
    @patch('builtins.print')
    def test_note_list_command(self, mock_print, mock_list):
        mock_list.return_value = ['Note 1', 'Note 2']
        with patch('sys.argv', ['cli.py', 'note', 'list']):
            main()
            mock_list.assert_called()
            mock_print.assert_called()

    @patch('assistant.cli.safe_calc')
    @patch('builtins.print')
    def test_calc_command(self, mock_print, mock_calc):
        mock_calc.return_value = 5
        with patch('sys.argv', ['cli.py', 'calc', '2+3']):
            main()
            mock_calc.assert_called_with('2+3')
            mock_print.assert_called_with('Result: 5')

    @patch('assistant.cli.get_answer')
    @patch('builtins.print')
    def test_ask_command(self, mock_print, mock_get):
        mock_get.return_value = 'Answer'
        with patch('sys.argv', ['cli.py', 'ask', 'Question']):
            main()
            mock_get.assert_called_with('Question', online=False)
            mock_print.assert_called_with('Answer')

if __name__ == '__main__':
    unittest.main()