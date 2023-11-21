import time
from message import Message
from user import User

def display_help(app, user: User, command_text):
    from bot_command_handler import get_allowed_commands, bot_commands
    allowed_commands = get_allowed_commands(user)
    response = "Here is a list of commands available to you: \n"
    command_list = ""
    for c in allowed_commands:
        response += "- `" + c + "` - " + bot_commands[c]["info"] + "\n"
        command_list += f"<{c}> "
    user.send_im_message(text=response)
    print(f"{time.ctime(time.time())}:{user.name} (is_bot_admin: {user.is_bot_admin}):Sent a List of Commands!:{command_list}")

def display_joke(app, user: User, command_text):
    import pyjokes
    new_joke = pyjokes.get_joke()
    user.send_im_message(new_joke)
    print(f"{time.ctime(time.time())}:{user.name}:Joke:{new_joke}")

def display_changelog(app, user: User, command_text):
    with open('changelog.txt') as f:
        lines = f.readlines()
    
    response = "```"
    for l in lines:
        response += l
    response += "```"
    user.send_im_message(response)
    print(f"{time.ctime(time.time())}:{user.name}:Changelog Sent!")

def display_admins(app, user: User, command_text):
    import random
    from user import get_user, bot_admins

    response = "Recognised Administrators of the Sitecore Community Slack are: \n\n"
    random_bot_admins = random.sample(bot_admins, len(bot_admins))

    for user_id in random_bot_admins:
        u = get_user(app, user_id)
        response += f"- {u.real_name} - <@{u.id}>\n"

    response += f"\nFeel free to reach out to any of them, if you have something on your mind in regards to this Sitecore Community Slack."
    user.send_im_message(response)
    print(f"{time.ctime(time.time())}:{user.name}:Was Sent a List of Admins!")

def display_channels(app, user: User, command_text, raw_list=False):
    from channel import Channel, get_channel

    if raw_list:
        user.send_im_message("This is gonna take a short while... hold on...")

    channel_types = "public_channel"
    if user.is_bot_admin:
        channel_types += ",private_channel"

    channel_list = []

    channel_info_list = app.client.conversations_list(limit=5000,types=channel_types)
    for ci in channel_info_list["channels"]:
        try:
            if ci["is_member"] or raw_list:
                c: Channel = get_channel(app, ci["id"])
                channel_list.append(c)
        except:
            print(f"is_member not present on {ci}")

    channel_list.sort(key=lambda x: x.name)
    
    if user.is_bot_admin:
        private_message = "(restricted/members-only channels are shown)"
    else:
        private_message = "(restricted/members-only channels are not shown)"

    if raw_list:
        response = f"Here is the full list of channels I am aware of. Member=✅, Private=🔒, Archived=🗑️\n\n"
    else:
        response = f"Here is the list of channels I am currently active in: {private_message}\n\n"

    for c in channel_list:
        response += f"- <#{c.id}> ({c.num_members} members) "
        if c.is_member:
            response += "✅"
        if c.is_private:
            response += "🔒"
        if c.is_archived:
            response += "🗑️"

        response += "\n"
    
    user.send_im_message(response)
    print(f"{time.ctime(time.time())}:{user.name}:Was Sent a List of Channels!")

def display_all_channels(app, user: User, command_text):
    display_channels(app, user, command_text, True)

def display_user_info(app, user: User, command_text):
    import re
    from user import User, get_user

    user_id_regex = "@\w+"
    response = ""
    found_users = 0

    for m in re.findall(user_id_regex, command_text):
        u: User = get_user(app, m[1:])
        if u:
            response += f"User: <@{u.id}> - Account Name: {u.name}, Real Name: {u.real_name}, Email: {u.email_address}\n"
            found_users += 1
        else:
            response += f"User ID: {m} not found!\n"

    response += "\nInformation given here is PII and should be treated as such! Don't share."

    if found_users > 0:
        user.send_im_message(response)
    else:
        user.send_im_message(f"Usage: lookup @user @user @user. Ex. 'lookup @mr.tamas.varga'")

    print(f"{time.ctime(time.time())}:{user.name}:Looked up users:{command_text}")

def register_feedback(app, user: User, command_text):
    # community-feedback-discussion
    feedback_channel = "C063MAHDS5U"

    feedback = command_text.split(" ", 1)
    if len(feedback) != 2:
        user.send_im_message("Usage: `feedback` your feedback here")
        return
    
    feedback = feedback[1]
    app.client.chat_postMessage(channel=feedback_channel, text=f"FEEDBACK: {feedback}", blocks=None)
    user.send_im_message("Your feedback has been shared with the Sitecore Community Slack team. Thank you!")

    # TODO: Anonymise, once we're happy it works as expected
    print(f"{time.ctime(time.time())}:{user.name}:Feedback Provided:{command_text}")

def display_stats(app, user: User, command_text):
    from bot_memory import stats_command

    USAGE_TEXT = "USAGE: stats MM YY. E.g. `stats 11 23` for November 2023. To sort by channel name, use `stats 11 23 channel`."
    cmd = command_text.split(" ")
    if len(cmd) < 3:
        user.send_im_message(USAGE_TEXT)
        return

    month = 0
    year = 0
    sort_by_channel_name = False
    try:
        month = int(cmd[1])
        year = int(cmd[2])
    except:
        user.send_im_message(USAGE_TEXT)

    if month < 1 or month > 12 or year > 30:
        user.send_im_message(USAGE_TEXT)
        return

    if len(cmd) > 3:
        sort_by_channel_name = True

    stats_command(app, user, command_text, month, year, sort_by_channel_name)
