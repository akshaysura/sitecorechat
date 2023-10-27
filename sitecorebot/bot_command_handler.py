from message import Message
from bot_commands import display_help, display_joke, display_changelog

bot_commands = {
    "help": {
        "requires_bot_admin": False,
        "allow_in_im": True,
        "allow_in_mpim": True,
        "callable": display_help
    },
    "joke": {
        "requires_bot_admin": False,
        "allow_in_im": True,
        "allow_in_mpim": True,
        "callable": display_joke
    },
    "changelog": {
        "requires_bot_admin": True,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "callable": display_changelog
    }
}

def bot_command_handler(message: Message):
    commands = get_allowed_commands(message)
    if len(commands) == 0: return

    # probably going to need argparse or arglite here

    lowercase_incoming_message = message.text.lower()
    if lowercase_incoming_message not in commands:
        # for now, the bot only handles direct IM commands
        if message.is_im:
            message.respond("I'm sorry, I don't understand!  For a list of commands available to you, type HELP")
    else:
        cmd = bot_commands[lowercase_incoming_message]["callable"]
        cmd(message)

def get_allowed_commands(message: Message) -> {}:
    allowed_commands = {}

    for c in bot_commands:
        allow = True
        if message.is_im: allow = bot_commands[c]["allow_in_im"]
        if allow:
            if message.is_mpim: allow = bot_commands[c]["allow_in_mpim"]
        if allow:
            if bot_commands[c]["requires_bot_admin"]: allow = message.user.is_bot_admin

        if allow:
            allowed_commands[c] = c

    return allowed_commands

print(f"Bot Command Handler Online. Commands:")
for c in bot_commands:
    print("- ", c, bot_commands[c])
