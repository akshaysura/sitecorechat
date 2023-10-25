BOT_VERSION = "0.1 alpha"

import os, re, time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from defs import *
from new_user_request import new_user_request
from hey_sitecorebot import hey_sitecorebot, joke

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

@app.message(re.compile("^joke$"))
def app_message_joke(message, say):
    joke(app, message, say)

# Universal listener, for debug and development purposes
# Only gets invoked if no previous handler has picked up the message
@app.message(re.compile("^."))
def all_message_handler(message, say):
    channel_id = message["channel"]
    channel_type = message["channel_type"]
    user_id = message["user"]
    userinfo = app.client.users_info(user=user_id)["user"]
    message_text = message["text"]
    timestamp = message["ts"]
    dt = time.ctime(float(timestamp))

    if channel_type != "im":
        channel = app.client.conversations_info(channel=channel_id, include_num_members=True)["channel"]
        print(f"Message '{message_text}' received in channel #{channel['name']} ({channel_id}) ({channel['num_members']} members) at {dt} from user {userinfo['name']} ({user_id})")
    else:
        print(f"Message '{message_text}' received in a direct message at {dt} from user {userinfo['name']} ({user_id})")


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

@app.event("reaction_added")
def handle_reaction_added_events(body, logger):
    print(body)
    print()

if __name__ == "__main__":
    print(f"Sitecore Community Slackbot {BOT_VERSION} starting...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
