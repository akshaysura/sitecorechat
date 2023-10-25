BOT_VERSION = "0.1 alpha"

import os, re, time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from defs import *
from new_user_request import new_user_request
from hey_sitecorebot import hey_sitecorebot

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

@app.message("New User Request")
def app_new_user_request(message, say):
    new_user_request(app, message, say)

@app.message(re.compile("([hH]ey|[hH]ello) [sS]itecore[bB]ot"))
def app_hey_sitecorebot(message, say):
    hey_sitecorebot(app, message, say)

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

# catch-all
@app.event("message")
def handle_message_events(body, logger):
    print(body)
    print()

# not doing anything with @mentions of the bot yet
@app.event("app_mention")
def handle_app_mention_events(body, logger):
    print(body)
    print()

if __name__ == "__main__":
    print(f"Sitecore Community Slackbot {BOT_VERSION} starting...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
