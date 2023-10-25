import re
from defs import channel_zinvite, channel_sitecorebot_sandbox, email_regex_pattern

# Will be listening to "New User Request in #zinvite and #sitecorebot-sandbox"
channel_zinvite_listeners = [channel_zinvite, channel_sitecorebot_sandbox]

def new_user_request(app, message, say):
    channel_id = message["channel"]
    message_text = message["text"]
    message_ts = message["ts"]

    if channel_id not in channel_zinvite_listeners:
        channel = app.client.conversations_info(channel=channel_id, include_num_members=True)["channel"]
        ignored_message = f"New User Request ignored in channel {channel['name']} ({channel_id})"
        app.logger.debug(ignored_message)
        print(ignored_message)
        return

    match = re.search(email_regex_pattern, message_text)
    if match:
        user_request_email = match.group()
        print(f"Incoming New User Request for Email {user_request_email}")
        try:
            userinfo_request = app.client.users_lookupByEmail(email=user_request_email)
            existing_userinfo = userinfo_request["user"]
            app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="red_circle")
            response_message = f"Found user as <@{existing_userinfo['id']}> ({existing_userinfo['real_name']})"
            say(text=response_message, thread_ts=message_ts)
            say(text = f"```{existing_userinfo}```", thread_ts=message_ts)
            print(response_message)
        except:
            # user was not found, this is good
            app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="large_green_circle")
            print(f"Incoming request for {user_request_email} is a new user")
