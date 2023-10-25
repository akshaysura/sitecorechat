import os, re, time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

bot_admins = ["U0D8XHJSH", "lala"]

# reference message pattern implementation
@app.message(re.compile("([hH]ey|[hH]ello) [sS]itecore[bB]ot"))
def app_sitecorebot_referred(message, say):
    if message["user"] not in bot_admins:
        print("Sitecorebot was called by a non-admin.")
    else:
        print("Sitecorebot was called by an admin")

# Universal listener, for debug and development purposes
# Only gets invoked if no previous handler has picked up the message
@app.message(re.compile("^."))
def all_message_handler(message, say):
    # see message.json
    message_id = message["client_msg_id"]
    message_text = message["text"]
    user_id = message["user"]
    # see userinfo.json
    userinfo = app.client.users_info(user=user_id)["user"]
    timestamp = message["ts"]
    dt = time.ctime(float(timestamp))
    channel_id = message["channel"]
    # see channelinfo.json
    channel = app.client.conversations_info(channel=channel_id, include_num_members=True)["channel"]
    print(f"Message id {message_id} received in channel #{channel['name']} ({channel_id}) ({channel['num_members']} members) at {dt}. '{message_text}' from user {userinfo['name']} ({user_id}).")

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
