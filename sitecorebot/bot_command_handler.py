from message import Message
from bot_commands import display_help, display_joke, display_changelog, display_admins, display_channels, display_all_channels, display_user_info, register_feedback
from welcome import display_welcome, display_rules

bot_commands = {
    "help": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": True,
        "info": "Displays a list of commands available to you.",
        "callable": display_help
    },
    "joke": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": True,
        "info": "Displays a random joke.",
        "callable": display_joke
    },
    "changelog": {
        "requires_bot_admin": True,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Displays the changelog for this bot.",
        "callable": display_changelog
    },
    "admins": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Lists the current admins for the Sitecore Community Slack.",
        "callable": display_admins
    },
    "channels": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Displays all channels this bot is currently registered in.",
        "callable": display_channels
    },
    "allchannels": {
        "requires_bot_admin": True,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Displays a list of all channels available on this Sitecore Community Slack",
        "callable": display_all_channels
    },
    "lookup": {
        "requires_bot_admin": False,
        "requires_community_coordinator": True,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Looks up user information based on a Slack user id. Ex.: `lookup @mr.tamas.varga`",
        "callable": display_user_info
    },
    "welcome": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Displays the welcome messaging sent to new users joining this Sitecore Community Slack.",
        "callable": display_welcome
    },
    "rules": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Displays the current rules and guidelines for this Sitecore Community Slack.",
        "callable": display_rules
    },
    "feedback": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "allow_in_im": True,
        "allow_in_mpim": False,
        "info": "Provide anonymous feedback to the people running this Sitecore Community Slack.",
        "callable": register_feedback
    }
}

def bot_command_handler(message: Message):
    if message.is_channel_message: return

    commands = get_allowed_commands(message)
    if len(commands) == 0: return

    # probably going to need argparse or arglite here

    lowercase_incoming_message = message.text.split(" ", 1)[0].lower()
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
            bot_commands[c]["requires_community_coordinator"]: allow = (message.user.is_bot_admin or message.user.is_community_coordinator)

        if allow:
            allowed_commands[c] = c

    return allowed_commands

print(f"Bot Command Handler Online. Commands:")
for c in bot_commands:
    print("- ", c, bot_commands[c])
