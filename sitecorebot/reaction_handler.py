from slack_bolt import App
from message import Message, get_message
from user import User, get_user, is_bot_admin_user, is_community_coordinator
from channel import Channel, get_channel
from expiring_dict import ExpiringDict

reaction_memory: ExpiringDict = ExpiringDict(3600*24)

def reaction_handler(app: App, user_id, reaction, item_user_id, channel_id, message_id):
    reacting_user = get_user(app, user_id)
    message_user = get_user(app, item_user_id)
    channel = get_channel(app, channel_id)
    print(f"User: {reacting_user.name} is reacting with :{reaction}: to {message_user.name}'s message in channel: {channel.name}")
    return 
    try:
        app.client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"Your reaction :{reaction}: has been recorded")
    except:
        pass
