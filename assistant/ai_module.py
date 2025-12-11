import re
import os
import datetime
import logging
from typing import Dict, Callable, Union, Optional

# Optional imports
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# Context for conversation
conversation_context: Dict[str, str] = {}

# Enhanced offline responses with more intelligence
OFFLINE_RESPONSES: Dict[re.Pattern, Union[str, Callable[[], str]]] = {
    re.compile(r'.*\b(name|who are you|what are you)\b.*', re.IGNORECASE): "I am Mini AI Assistant, your intelligent offline helper.",
    re.compile(r'.*\b(how are you|hello|hi|hey)\b.*', re.IGNORECASE): "Hello! I'm doing great, ready to assist you.",
    re.compile(r'.*\b(time|what time|current time)\b.*', re.IGNORECASE): lambda: f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}.",
    re.compile(r'.*\b(date|what date|today)\b.*', re.IGNORECASE): lambda: f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}.",
    re.compile(r'.*\b(weather|forecast)\b.*', re.IGNORECASE): "I'm offline; I can't check the weather. Try online mode for real-time data.",
    re.compile(r'.*\b(joke|funny)\b.*', re.IGNORECASE): "Why don't scientists trust atoms? Because they make up everything!",
    re.compile(r'.*\b(help|what can you do)\b.*', re.IGNORECASE): "I can help with reminders, notes, calculations, and Q&A. Use 'ask' command!",
    re.compile(r'.*\b(thank|thanks)\b.*', re.IGNORECASE): "You're welcome! Happy to help.",
    re.compile(r'.*\b(bye|goodbye|exit)\b.*', re.IGNORECASE): "Goodbye! Have a great day.",
    re.compile(r'.*\b(calculate|math|compute)\b.*', re.IGNORECASE): "Use the 'calc' command for calculations.",
    re.compile(r'.*\b(remind|reminder)\b.*', re.IGNORECASE): "Use 'remind' to schedule reminders.",
    re.compile(r'.*\b(note|notes)\b.*', re.IGNORECASE): "Use 'note add' to save notes, 'note list' to view them.",
}

def get_offline_answer(question: str) -> str:
    """
    Get an intelligent answer using offline keyword-based logic with context.

    Args:
        question (str): The user's question.

    Returns:
        str: The response.
    """
    # Check for context (e.g., follow-up questions)
    if 'last_topic' in conversation_context:
        if re.search(r'\b(more|tell me|explain)\b', question, re.IGNORECASE):
            topic = conversation_context['last_topic']
            if topic == 'time':
                return f"More precisely, it's {datetime.datetime.now().strftime('%H:%M:%S %Z')}."
            elif topic == 'date':
                return f"It's {datetime.datetime.now().strftime('%A, %B %d, %Y')}."

    for pattern, response in OFFLINE_RESPONSES.items():
        if pattern.search(question):
            # Update context
            if 'time' in question.lower():
                conversation_context['last_topic'] = 'time'
            elif 'date' in question.lower():
                conversation_context['last_topic'] = 'date'
            else:
                conversation_context.pop('last_topic', None)

            if callable(response):
                return response()
            return response

    # Fallback with suggestions
    return "I'm sorry, I don't understand that. Try asking about time, date, reminders, or use online mode for advanced queries."

def get_online_answer(question: str, provider: str = "openai") -> str:
    """
    Get an answer using online API with improved error handling.

    Args:
        question (str): The user's question.
        provider (str): 'openai' or 'gemini'.

    Returns:
        str: The response or error message.
    """
    if not REQUESTS_AVAILABLE:
        return "Requests library not available for online queries."

    if provider == "openai" and OPENAI_AVAILABLE:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "OpenAI API key not set. Set OPENAI_API_KEY environment variable."
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Faster model
                messages=[{"role": "user", "content": question}],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            return f"Error querying OpenAI: {str(e)}"

    elif provider == "gemini" and GENAI_AVAILABLE:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Gemini API key not set. Set GEMINI_API_KEY environment variable."
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(question)
            return response.text.strip()
        except Exception as e:
            logging.error(f"Gemini error: {e}")
            return f"Error querying Gemini: {str(e)}"

    return "Online provider not available or not supported."

def get_answer(question: str, online: bool = False) -> str:
    """
    Get an answer, preferring online if requested, with intelligent fallback.

    Args:
        question (str): The user's question.
        online (bool): Whether to use online APIs.

    Returns:
        str: The response.
    """
    if online:
        answer = get_online_answer(question)
        if not answer.startswith("Error") and not answer.startswith("Online"):
            return f"[ONLINE] {answer}"
        logging.warning("Online query failed, falling back to offline.")
    return f"[OFFLINE] {get_offline_answer(question)}"