import unittest
from unittest.mock import patch
from assistant.ai_module import get_offline_answer, get_answer, conversation_context

class TestAIModule(unittest.TestCase):
    def setUp(self):
        conversation_context.clear()

    def test_get_offline_answer_known(self):
        answer = get_offline_answer('What is your name?')
        self.assertIn('Mini AI Assistant', answer)

    def test_get_offline_answer_joke(self):
        answer = get_offline_answer('Tell me a joke')
        self.assertIn('scientists', answer)

    def test_get_offline_answer_context(self):
        get_offline_answer('What time is it?')
        answer = get_offline_answer('Tell me more')
        self.assertIn('precisely', answer)

    def test_get_offline_answer_unknown(self):
        answer = get_offline_answer('Unknown question xyz')
        self.assertIn("don't understand", answer)

    def test_get_answer_offline(self):
        answer = get_answer('Hello', online=False)
        self.assertIn('[OFFLINE]', answer)
        self.assertIn('Hello', answer)

    @unittest.skipUnless(__import__('assistant.ai_module', fromlist=['OPENAI_AVAILABLE']).OPENAI_AVAILABLE, "OpenAI not available")
    def test_get_answer_online_success(self):
        # Mock the availability
        import assistant.ai_module as ai_mod
        with patch('openai.OpenAI') as mock_client:
            mock_instance = mock_client.return_value
            mock_response = mock_instance.chat.completions.create.return_value
            mock_response.choices[0].message.content = "Online response"
            answer = get_answer('Question', online=True)
            self.assertIn('[ONLINE]', answer)
            self.assertIn('Online response', answer)

    @patch('assistant.ai_module.get_online_answer')
    def test_get_answer_online_fallback(self, mock_online):
        mock_online.return_value = "Error: No key"
        answer = get_answer('Question', online=True)
        self.assertIn('[OFFLINE]', answer)

if __name__ == '__main__':
    unittest.main()