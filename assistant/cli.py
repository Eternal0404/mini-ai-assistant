import argparse
import sys
from assistant.utils import add_note, list_notes, schedule_reminder, check_reminders, safe_calc
from assistant.ai_module import get_answer

def main():
    parser = argparse.ArgumentParser(description="Mini AI Assistant CLI")
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

    # Check reminders (implicit command)
    check_parser = subparsers.add_parser('check', help='Check for due reminders')

    args = parser.parse_args()

    if args.command == 'remind':
        try:
            schedule_reminder(args.message, args.time)
            print(f"Reminder scheduled: {args.message} at {args.time}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif args.command == 'note':
        if args.note_command == 'add':
            add_note(args.note)
            print("Note added.")
        elif args.note_command == 'list':
            notes = list_notes()
            if notes:
                for i, note in enumerate(notes, 1):
                    print(f"{i}. {note}")
            else:
                print("No notes found.")
        else:
            note_parser.print_help()
    
    elif args.command == 'calc':
        result = safe_calc(args.expression)
        print(f"Result: {result}")
    
    elif args.command == 'ask':
        answer = get_answer(args.question, online=args.online)
        print(answer)
    
    elif args.command == 'check':
        check_reminders()
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()