import json
import os
import ast
import datetime
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_DIR = 'data'

def ensure_data_dir():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_data(file_path: str, data: dict) -> None:
    """
    Save data to a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        data (dict): Data to save.

    Raises:
        IOError: If writing to file fails.
    """
    ensure_data_dir()
    full_path = os.path.join(DATA_DIR, file_path)
    try:
        with open(full_path, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data saved to {full_path}")
    except IOError as e:
        logging.error(f"Failed to save data to {full_path}: {e}")
        raise

def load_data(file_path: str) -> dict:
    """
    Load data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded data, or empty dict if file missing or corrupted.
    """
    full_path = os.path.join(DATA_DIR, file_path)
    try:
        with open(full_path, 'r') as f:
            data = json.load(f)
        logging.info(f"Data loaded from {full_path}")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.warning(f"Failed to load data from {full_path}: {e}. Returning empty dict.")
        return {}

def add_note(note: str) -> None:
    """
    Add a note to the notes file.

    Args:
        note (str): The note to add.
    """
    notes = load_data('notes.json')
    if 'notes' not in notes:
        notes['notes'] = []
    notes['notes'].append(note)
    save_data('notes.json', notes)

def list_notes() -> list[str]:
    """
    List all notes.

    Returns:
        list[str]: List of notes.
    """
    notes = load_data('notes.json')
    return notes.get('notes', [])

def schedule_reminder(message: str, time_str: str) -> None:
    """
    Schedule a reminder at the specified time.

    Args:
        message (str): Reminder message.
        time_str (str): Time in HH:MM format.

    Raises:
        ValueError: If time format is invalid.
    """
    try:
        time_obj = datetime.datetime.strptime(time_str, '%H:%M').time()
        now = datetime.datetime.now()
        reminder_time = datetime.datetime.combine(now.date(), time_obj)
        if reminder_time < now:
            reminder_time += datetime.timedelta(days=1)  # Next day if time passed
        delay = (reminder_time - now).total_seconds()
        
        reminders = load_data('reminders.json')
        if 'reminders' not in reminders:
            reminders['reminders'] = []
        reminders['reminders'].append({'message': message, 'time': time_str, 'scheduled_at': reminder_time.isoformat()})
        save_data('reminders.json', reminders)
        
        threading.Timer(delay, lambda: print(f"Reminder: {message}")).start()
        logging.info(f"Reminder scheduled for {time_str}: {message}")
    except ValueError as e:
        logging.error(f"Invalid time format {time_str}: {e}")
        raise

def check_reminders() -> None:
    """
    Check and alert for due reminders, then remove them.
    """
    reminders = load_data('reminders.json')
    if 'reminders' not in reminders:
        return
    now = datetime.datetime.now()
    updated_reminders = []
    for rem in reminders['reminders']:
        rem_time = datetime.datetime.fromisoformat(rem['scheduled_at'])
        if rem_time <= now:
            print(f"Reminder: {rem['message']}")
            logging.info(f"Reminder triggered: {rem['message']}")
        else:
            updated_reminders.append(rem)
    reminders['reminders'] = updated_reminders
    save_data('reminders.json', reminders)

def safe_calc(expression: str) -> float | str:
    """
    Safely evaluate a mathematical expression.

    Args:
        expression (str): The expression to evaluate.

    Returns:
        float | str: Result or error message.
    """
    try:
        # Use eval with restricted environment for basic math
        import math
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'math': math,
            '__builtins__': {}
        }
        result = eval(expression, safe_dict)
        if isinstance(result, (int, float)):
            return result
        else:
            return "Error: Expression must evaluate to a number."
    except Exception as e:
        logging.error(f"Calculation error for '{expression}': {e}")
        return f"Error: {str(e)}"