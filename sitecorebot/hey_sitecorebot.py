import time
import pyjokes
from channel import Channel, get_channel
from user import User, get_user

def hey_sitecorebot(app, message, say):
    channel: Channel = get_channel(app, message["channel"])
    user: User = get_user(app, message["user"])
    message_ts = message["ts"]

    if not user.is_bot_admin:
        app.client.reactions_add(channel=channel.id, timestamp=message_ts, name="thumbsdown")
    else:
        app.client.reactions_add(channel=channel.id, timestamp=message_ts, name="thumbsup")

def joke(app, message, say):
    # Only respond in private chat
    channel: Channel = get_channel(app, message["channel"])
    if not channel.is_direct_messaging:
        return

    user: User = get_user(app, message["user"])
    timestamp = message["ts"]
    dt = time.ctime(float(timestamp))

    new_joke = pyjokes.get_joke()
    say(text=new_joke, channel=channel.id)
    print(f"{dt}:{user.name}:Joke:{new_joke}")

def changelog(app, message, say):
    pass
