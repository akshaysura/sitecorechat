from message import Message

def display_help(message: Message):
    from bot_command_handler import get_allowed_commands, bot_commands
    allowed_commands = get_allowed_commands(message)
    response = "Here is a list of commands available to you: \n"
    command_list = ""
    for c in allowed_commands:
        response += "- " + c + "\n"
        command_list += f"<{c}> "
    message.respond(response)
    print(f"{message.message_date_time_string}:{message.user.name} (is_bot_admin: {message.user.is_bot_admin}):Sent a List of Commands!:{command_list}")

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

def display_admins(message: Message):
    import random
    from user import get_user, bot_admins

    response = "Recognised Administrators of the Sitecore Community Slack are: \n\n"
    random_bot_admins = random.sample(bot_admins, len(bot_admins))

    for user_id in random_bot_admins:
        u = get_user(message._app, user_id)
        response += f"- {u.real_name} - <@{u.id}>\n"

    response += f"\nFeel free to reach out to any of them, if you have something on your mind in regards to this Sitecore Community Slack."
    message.respond(response)
    print(f"{message.message_date_time_string}:{message.user.name}:Was Sent a List of Admins!")
