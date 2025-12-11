import re
import os
import datetime
import logging

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

# Offline responses
OFFLINE_RESPONSES = {
    re.compile(r'.*\b(name|who are you)\b.*', re.IGNORECASE): "I am Mini AI Assistant.",
    re.compile(r'.*\b(how are you|hello|hi)\b.*', re.IGNORECASE): "Hello! I'm doing well, thank you.",
    re.compile(r'.*\b(time|what time)\b.*', re.IGNORECASE): lambda: f"The current time is {datetime.datetime.now().strftime('%H:%M')}.",
    re.compile(r'.*\b(date|what date)\b.*', re.IGNORECASE): lambda: f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}.",
    re.compile(r'.*\b(weather)\b.*', re.IGNORECASE): "I'm offline; I can't check the weather. Try online mode.",
}

def get_offline_answer(question: str) -> str:
    """
    Get an answer using offline keyword-based logic.

    Args:
        question (str): The user's question.

    Returns:
        str: The response.
    """
    for pattern, response in OFFLINE_RESPONSES.items():
        if pattern.search(question):
            if callable(response):
                return response()
            return response
    return "I'm sorry, I don't understand that question. Try asking something else or use online mode."

def get_online_answer(question: str, provider: str = "openai") -> str:
    """
    Get an answer using online API.

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
            return "OpenAI API key not set."
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            return "Error querying OpenAI."
    
    elif provider == "gemini" and GENAI_AVAILABLE:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Gemini API key not set."
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(question)
            return response.text.strip()
        except Exception as e:
            logging.error(f"Gemini error: {e}")
            return "Error querying Gemini."
    
    return "Online provider not available or not supported."

def get_answer(question: str, online: bool = False) -> str:
    """
    Get an answer, preferring online if requested.

    Args:
        question (str): The user's question.
        online (bool): Whether to use online APIs.

    Returns:
        str: The response.
    """
    if online:
        answer = get_online_answer(question)
        if not answer.startswith("Error") and not answer.startswith("Online"):
            return answer
        # Fallback to offline
    return get_offline_answer(question)