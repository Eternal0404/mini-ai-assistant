import unittest
from assistant.ai_module import get_offline_answer, get_answer

class TestAIModule(unittest.TestCase):
    def test_get_offline_answer_known(self):
        answer = get_offline_answer('What is your name?')
        self.assertIn('Mini AI Assistant', answer)

    def test_get_offline_answer_unknown(self):
        answer = get_offline_answer('Unknown question')
        self.assertIn("don't understand", answer)

    def test_get_answer_offline(self):
        answer = get_answer('Hello', online=False)
        self.assertIn('Hello', answer)

    # Online tests would require mocking, but skip for now

if __name__ == '__main__':
    unittest.main()