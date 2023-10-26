import time
import pyjokes
from channel import Channel, get_channel
from user import User, get_user

def hey_sitecorebot(app, message, say):
    user: User = get_user(app, message["user"])
    if not user: return

    message_ts = message["ts"]

    if not user.is_bot_admin:
        app.client.reactions_add(channel=message["channel"], timestamp=message_ts, name="thumbsdown")
    else:
        app.client.reactions_add(channel=message["channel"], timestamp=message_ts, name="thumbsup")

def joke(app, message, say):
    # Only respond in private chat
    if message["channel_type"] not in ["im", "mpim"]: return
    user: User = get_user(app, message["user"])
    if not user: return

    timestamp = message["ts"]
    dt = time.ctime(float(timestamp))

    new_joke = pyjokes.get_joke()
    say(text=new_joke, channel=message["channel"])
    print(f"{dt}:{user.name}:Joke:{new_joke}")

def changelog(app, message, say):
    pass
