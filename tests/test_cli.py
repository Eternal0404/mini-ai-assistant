import unittest
import sys
from unittest.mock import patch
from assistant.cli import main

class TestCLI(unittest.TestCase):
    @patch('assistant.cli.schedule_reminder')
    @patch('assistant.cli.print_success')
    def test_remind_command(self, mock_print, mock_schedule):
        with patch('sys.argv', ['cli.py', 'remind', 'Test message', '--time', '10:00']):
            main()
            mock_schedule.assert_called_with('Test message', '10:00')
            mock_print.assert_called_with("Reminder scheduled: 'Test message' at 10:00")

    @patch('assistant.cli.add_note')
    @patch('assistant.cli.print_success')
    def test_note_add_command(self, mock_print, mock_add):
        with patch('sys.argv', ['cli.py', 'note', 'add', 'Test note']):
            main()
            mock_add.assert_called_with('Test note')
            mock_print.assert_called_with('Note added successfully.')

    @patch('assistant.cli.list_notes')
    @patch('assistant.cli.display_notes')
    def test_note_list_command(self, mock_display, mock_list):
        mock_list.return_value = ['Note 1', 'Note 2']
        with patch('sys.argv', ['cli.py', 'note', 'list']):
            main()
            mock_list.assert_called()
            mock_display.assert_called_with(['Note 1', 'Note 2'])

    @patch('assistant.cli.safe_calc')
    @patch('assistant.cli.print_success')
    def test_calc_command(self, mock_print, mock_calc):
        mock_calc.return_value = 5
        with patch('sys.argv', ['cli.py', 'calc', '2+3']):
            main()
            mock_calc.assert_called_with('2+3')
            mock_print.assert_called_with('Result: 5')

    @patch('assistant.cli.safe_calc')
    @patch('assistant.cli.print_error')
    def test_calc_command_error(self, mock_print, mock_calc):
        mock_calc.return_value = "Error: Invalid"
        with patch('sys.argv', ['cli.py', 'calc', 'invalid']):
            main()
            mock_calc.assert_called_with('invalid')
            mock_print.assert_called_with('Error: Invalid')

    @patch('assistant.cli.get_answer')
    @patch('assistant.cli.print_info')
    def test_ask_command(self, mock_print, mock_get):
        mock_get.return_value = '[OFFLINE] Answer'
        with patch('sys.argv', ['cli.py', 'ask', 'Question']):
            main()
            mock_get.assert_called_with('Question', online=False)
            mock_print.assert_called_with('[OFFLINE] Answer')

    @patch('assistant.cli.check_reminders')
    @patch('assistant.cli.print_info')
    def test_check_command(self, mock_print, mock_check):
        with patch('sys.argv', ['cli.py', 'check']):
            main()
            mock_check.assert_called()
            mock_print.assert_called_with('Reminders checked.')

if __name__ == '__main__':
    unittest.main()