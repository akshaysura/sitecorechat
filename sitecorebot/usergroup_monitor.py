from message import Message

usergroup_monitor_alert_channel = "C0625KEQ2VD"

def usergroup_monitor(message: Message):
    message.respond_to_channel(usergroup_monitor_alert_channel, f"USERGROUP MESSAGE (suspected): {message.get_permalink()} in channel <#{message.channel_id}>.")
    print(f"USER GROUP MONITOR: Flagged Message {message}")

print(f"Usergroup Monitor Online. Target Channel: {usergroup_monitor_alert_channel}.")

