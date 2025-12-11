import argparse
import sys
from typing import List
from assistant.utils import add_note, list_notes, schedule_reminder, check_reminders, safe_calc
from assistant.ai_module import get_answer

# Optional UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False

def print_success(message: str) -> None:
    if RICH_AVAILABLE:
        console.print(f"[green]+[/green] {message}")
    else:
        print(f"+ {message}")

def print_error(message: str) -> None:
    if RICH_AVAILABLE:
        console.print(f"[red]-[/red] {message}")
    else:
        print(f"- {message}")

def print_info(message: str) -> None:
    if RICH_AVAILABLE:
        console.print(f"[blue]i[/blue] {message}")
    else:
        print(f"i {message}")

def display_notes(notes: List[str]) -> None:
    if RICH_AVAILABLE:
        table = Table(title="Your Notes")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Note", style="magenta")
        for i, note in enumerate(notes, 1):
            table.add_row(str(i), note)
        console.print(table)
    else:
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mini AI Assistant - Intelligent CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m assistant.cli remind "Meeting" --time 14:00
  python -m assistant.cli note add "Buy groceries"
  python -m assistant.cli calc "2 + 3 * 4"
  python -m assistant.cli ask "What time is it?" --online
        """
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Remind command
    remind_parser = subparsers.add_parser('remind', help='Schedule a reminder')
    remind_parser.add_argument('message', help='Reminder message')
    remind_parser.add_argument('--time', required=True, help='Time in HH:MM format')

    # Note command
    note_parser = subparsers.add_parser('note', help='Manage notes')
    note_subparsers = note_parser.add_subparsers(dest='note_command', help='Note subcommands')

    add_parser = note_subparsers.add_parser('add', help='Add a note')
    add_parser.add_argument('note', help='The note to add')

    list_parser = note_subparsers.add_parser('list', help='List all notes')

    # Calc command
    calc_parser = subparsers.add_parser('calc', help='Evaluate a mathematical expression')
    calc_parser.add_argument('expression', help='Mathematical expression to evaluate')

    # Ask command
    ask_parser = subparsers.add_parser('ask', help='Ask a question')
    ask_parser.add_argument('question', help='The question to ask')
    ask_parser.add_argument('--online', action='store_true', help='Use online AI if available')

    # Check reminders
    check_parser = subparsers.add_parser('check', help='Check for due reminders')

    args = parser.parse_args()

    if args.command == 'remind':
        try:
            schedule_reminder(args.message, args.time)
            print_success(f"Reminder scheduled: '{args.message}' at {args.time}")
        except ValueError as e:
            print_error(f"Invalid time format: {e}")
            sys.exit(1)

    elif args.command == 'note':
        if args.note_command == 'add':
            add_note(args.note)
            print_success("Note added successfully.")
        elif args.note_command == 'list':
            notes = list_notes()
            if notes:
                display_notes(notes)
            else:
                print_info("No notes found. Add some with 'note add'.")
        else:
            note_parser.print_help()

    elif args.command == 'calc':
        result = safe_calc(args.expression)
        if isinstance(result, (int, float)):
            print_success(f"Result: {result}")
        else:
            print_error(result)

    elif args.command == 'ask':
        answer = get_answer(args.question, online=args.online)
        print_info(answer)

    elif args.command == 'check':
        check_reminders()
        print_info("Reminders checked.")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()