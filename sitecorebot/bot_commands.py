from message import Message

def display_help(message: Message):
    from bot_command_handler import get_allowed_commands
    allowed_commands = get_allowed_commands(message)
    response = "Here is a list of commands available to you: \n"
    for c in allowed_commands:
        response += "- " + c + "\n"
    message.respond(response)
    print(f"{message.message_date_time_string}:{message.user.name}:Sent a List of Commands!")

def display_joke(message: Message):
    import pyjokes
    new_joke = pyjokes.get_joke()
    message.respond(new_joke)
    print(f"{message.message_date_time_string}:{message.user.name}:Joke:{new_joke}")

def display_changelog(message: Message):
    with open('changelog.txt') as f:
        lines = f.readlines()
    
    response = "```"
    for l in lines:
        response += l
    response += "```"
    message.respond(response)

    print(f"{message.message_date_time_string}:{message.user.name}:Changelog Sent!")
