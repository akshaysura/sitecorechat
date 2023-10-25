from defs import bot_admins

def hey_sitecorebot(app, message, say):
    channel_id = message["channel"]
    message_ts = message["ts"]

    if message["user"] not in bot_admins:
        app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="thumbsdown")
    else:
        app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="thumbsup")
