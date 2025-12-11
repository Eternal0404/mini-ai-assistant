import unittest
import os
import tempfile
import shutil
from assistant.utils import save_data, load_data, add_note, list_notes, safe_calc, schedule_reminder, check_reminders

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Mock the DATA_DIR
        import assistant.utils
        assistant.utils.DATA_DIR = self.test_dir

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_load_data(self):
        data = {'test': 'value'}
        save_data('test.json', data)
        loaded = load_data('test.json')
        self.assertEqual(loaded, data)

    def test_load_data_missing(self):
        loaded = load_data('missing.json')
        self.assertEqual(loaded, {})

    def test_add_list_notes(self):
        add_note('Test note')
        notes = list_notes()
        self.assertIn('Test note', notes)

    def test_safe_calc_valid(self):
        result = safe_calc('2 + 3')
        self.assertEqual(result, 5)

    def test_safe_calc_invalid(self):
        result = safe_calc('invalid')
        self.assertIn('Error', result)

    def test_schedule_reminder(self):
        # Mock time to avoid actual scheduling
        import datetime
        from unittest.mock import patch
        with patch('assistant.utils.datetime') as mock_dt:
            mock_dt.datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0)
            mock_dt.datetime.combine.return_value = datetime.datetime(2023, 1, 1, 10, 5)
            mock_dt.timedelta = datetime.timedelta
            mock_dt.datetime.fromisoformat = datetime.datetime.fromisoformat
            schedule_reminder('Test reminder', '10:05')
            # Check if saved
            reminders = load_data('reminders.json')
            self.assertIn('reminders', reminders)

    def test_check_reminders(self):
        # Add a past reminder
        import datetime
        from unittest.mock import patch
        with patch('assistant.utils.datetime') as mock_dt, patch('builtins.print') as mock_print:
            mock_dt.datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 10)
            mock_dt.datetime.fromisoformat.return_value = datetime.datetime(2023, 1, 1, 10, 5)
            mock_dt.timedelta = datetime.timedelta
            # Simulate saved reminder
            reminders = {'reminders': [{'message': 'Past reminder', 'time': '10:05', 'scheduled_at': '2023-01-01T10:05:00'}]}
            save_data('reminders.json', reminders)
            check_reminders()
            mock_print.assert_called_with('[REMINDER] Past reminder')

if __name__ == '__main__':
    unittest.main()