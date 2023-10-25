import pyjokes

from defs import bot_admins

def hey_sitecorebot(app, message, say):
    channel_id = message["channel"]
    message_ts = message["ts"]

    if message["user"] not in bot_admins:
        app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="thumbsdown")
    else:
        app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="thumbsup")

def joke(app, message, say):
    # Only respond in private chat
    channel_type = message["channel_type"]
    if channel_type != "im":
        return
    
    dm_channel = message["channel"]
    user_id = message["user"]

    new_joke = pyjokes.get_joke()
    say(text=new_joke, channel=dm_channel)

    print(f"Sent joke < {new_joke} to user {user_id}")
