from message import Message

def hey_sitecorebot(message: Message):
    if not message.user: return

    if not message.user.is_bot_admin:
        message.react("thumbsdown")
    else:
        message.react("thumbsup")
