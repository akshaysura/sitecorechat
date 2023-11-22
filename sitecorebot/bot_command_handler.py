from user import User, get_user
from bot_commands import    display_help, display_joke, display_changelog, display_admins, display_channels, display_all_channels, \
                            display_user_info, register_feedback, display_stats
from welcome import display_welcome, display_rules

bot_commands = {
    "help": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Displays a list of commands available to you.",
        "callable": display_help
    },
    "joke": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Displays a random joke.",
        "callable": display_joke
    },
    "changelog": {
        "requires_bot_admin": True,
        "requires_community_coordinator": False,
        "info": "Displays the changelog for this bot.",
        "callable": display_changelog
    },
    "admins": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Lists the current admins for the Sitecore Community Slack.",
        "callable": display_admins
    },
    "channels": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Displays all channels this bot is currently registered in.",
        "callable": display_channels
    },
    "allchannels": {
        "requires_bot_admin": True,
        "requires_community_coordinator": False,
        "info": "Displays a list of all channels available on this Sitecore Community Slack",
        "callable": display_all_channels
    },
    "lookup": {
        "requires_bot_admin": False,
        "requires_community_coordinator": True,
        "info": "Looks up user information based on a Slack user id. Ex.: `lookup @mr.tamas.varga`",
        "callable": display_user_info
    },
    "welcome": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Displays the welcome messaging sent to new users joining this Sitecore Community Slack.",
        "callable": display_welcome
    },
    "rules": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Displays the current rules and guidelines for this Sitecore Community Slack.",
        "callable": display_rules
    },
    "feedback": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Provide anonymous feedback to the people running this Sitecore Community Slack.",
        "callable": register_feedback
    },
    "stats": {
        "requires_bot_admin": False,
        "requires_community_coordinator": False,
        "info": "Message Statistics for the Sitecore Community Slack.",
        "callable": display_stats
    },
}

def bot_command_handler(app, user_id, command_text):
    """Main entry point for all bot commands. Uses the user_id to determine which commands are available to that user, and will parse the command itself from command_text"""
    user: User = get_user(app, user_id)
    if not user:
        print(f"ERROR: INCOMING COMMAND USER NOT FOUND: {user_id}")
        return

    commands = get_allowed_commands(user)
    if len(commands) == 0: return

    lowercase_incoming_message = command_text.split(" ", 1)[0].lower()
    if lowercase_incoming_message not in commands:
        user.send_im_message("I'm sorry, I don't understand!  For a list of commands available to you, type HELP")
    else:
        cmd = bot_commands[lowercase_incoming_message]["callable"]
        cmd(app, user, command_text)

def get_allowed_commands(user: User) -> {}:
    allowed_commands = {}

    for c in bot_commands:
        allow = True
        if bot_commands[c]["requires_bot_admin"]: allow = user.is_bot_admin
        if allow:
            bot_commands[c]["requires_community_coordinator"]: allow = (user.is_bot_admin or user.is_community_coordinator)

        if allow:
            allowed_commands[c] = c

    return allowed_commands

print(f"Bot Command Handler Online. Commands:")
for c in bot_commands:
    print("- ", c, bot_commands[c])
