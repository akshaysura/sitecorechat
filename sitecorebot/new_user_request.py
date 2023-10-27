import re
from message import Message
from user import User, get_user_by_email

channel_sitecorebot_sandbox = "C0625KEQ2VD"
channel_sitecorebot_sandbox2 = "C062W6QCGGL"
channel_zinvite = "CA6SNF4NQ"

email_regex_pattern = "[\w\.-]+@[\w\.-]+\.\w+"

# Will be listening to "New User Request in #zinvite and #sitecorebot-sandbox"
channel_zinvite_listeners = [channel_zinvite, channel_sitecorebot_sandbox, channel_sitecorebot_sandbox2]

def new_user_request(m: Message):
    # New User Request would not happen in DMs
    if m.is_direct_message: return

    # New User Requests should only be acted on, in our defined list of channels
    if m.channel_id not in channel_zinvite_listeners: return

    match = re.search(email_regex_pattern, m.text)
    if match:
        user_request_email = match.group()
        u: User = get_user_by_email(m._app, user_request_email)

        if u:
            m.react("red_circle")
            m.respond_in_thread(f"Found user as <@{u.id}> ({u.name})")
            print(f"{m.message_date_time_string}:New User Request:{user_request_email}:Found Existing:{u.id} ({u.name})")
        else:
            # user was not found, this is good
            m.react("large_green_circle")
            print(f"{m.message_date_time_string}:New User Request:{user_request_email}:No Existing User Found")
