from message import Message

def display_help(message: Message):
    from bot_command_handler import get_allowed_commands, bot_commands
    allowed_commands = get_allowed_commands(message)
    response = "Here is a list of commands available to you: \n"
    command_list = ""
    for c in allowed_commands:
        response += "- `" + c + "` - " + bot_commands[c]["info"] + "\n"
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

def display_channels(message: Message, raw_list=False):
    from channel import Channel, get_channel

    if raw_list:
        message.respond("This is gonna take a short while... hold on...")

    channel_types = "public_channel"
    if message.user.is_bot_admin:
        channel_types += ",private_channel"

    channel_list = []

    channel_info_list = message._app.client.conversations_list(limit=5000,types=channel_types)
    for ci in channel_info_list["channels"]:
        try:
            if ci["is_member"] or raw_list:
                c: Channel = get_channel(message._app, ci["id"])
                channel_list.append(c)
        except:
            print(f"is_member not present on {ci}")

    channel_list.sort(key=lambda x: x.name)
    
    if message.user.is_bot_admin:
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
    
    message.respond(response)
    print(f"{message.message_date_time_string}:{message.user.name}:Was Sent a List of Channels!")

def display_all_channels(message: Message):
    display_channels(message, True)

def display_user_info(message: Message):
    import re
    from user import User, get_user

    user_id_regex = "@\w+"
    response = ""
    found_users = 0

    for m in re.findall(user_id_regex, message.text):
        u: User = get_user(message._app, m[1:])
        if u:
            response += f"User: <@{u.id}> - Account Name: {u.name}, Real Name: {u.real_name}, Email: {u.email_address}\n"
            found_users += 1
        else:
            response += f"User ID: {m} not found!\n"

    response += "\nInformation given here is PII and should be treated as such! Don't share."

    if found_users > 0:
        message.respond(response)
    else:
        message.respond(f"Usage: lookup @user @user @user. Ex. 'lookup @mr.tamas.varga'")

    print(f"{message.message_date_time_string}:{message.user.name}:Looked up users:{message.text}")

def register_feedback(message: Message):
    # community-feedback-discussion
    feedback_channel = "C063MAHDS5U"

    feedback = message.text.split(" ", 1)
    if len(feedback) != 2:
        message.respond("Usage: `feedback` your feedback here")
        return
    
    feedback = feedback[1]
    message.respond_to_channel(feedback_channel, f"FEEDBACK: {feedback}")
    message.respond("Your feedback has been shared with the Sitecore Community Slack team. Thank you!")

    # TODO: Anonymise, once we're happy it works as expected
    print(f"{message.message_date_time_string}:{message.user.name}:Feedback Provided:{message.text}")

def display_stats(message: Message):
    from bot_memory import stats_command

    USAGE_TEXT = "USAGE: stats MM YY. E.g. `stats 11 23` for November 2023. To sort by channel name, use `stats 11 23 channel`."
    cmd = message.text.split(" ")
    if len(cmd) < 3:
        message.respond(USAGE_TEXT)
        return

    month = 0
    year = 0
    sort_by_channel_name = False
    try:
        month = int(cmd[1])
        year = int(cmd[2])
    except:
        message.respond(USAGE_TEXT)

    if month < 1 or year > 30:
        message.respond(USAGE_TEXT)
        return

    if len(cmd) > 3:
        sort_by_channel_name = True

    stats_command(message, month, year, sort_by_channel_name)
