BOT_VERSION = "0.2 alpha - now with crosspost guardian"

import os, re, time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from new_user_request import new_user_request
from hey_sitecorebot import hey_sitecorebot, joke
from crosspost_guardian import crosspost_guardian
from message import Message

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

@app.message("New User Request")
def app_new_user_request(message, say):
    m: Message = Message(app, message, say)
    new_user_request(m)

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
    m: Message = Message(app, message, say)

    if m.is_channel_message:
        fuzzy_score = crosspost_guardian(m)
        print(f"{m.message_date_time_string}:#{m.channel.name} ({m.channel_id}):{m.user.name} ({m.user.id}):{m.text} [{fuzzy_score}]")
    else:
        print(f"{m.message_date_time_string}:IM/MPIM:{m.user.name} ({m.user.id}):{m.text}")

# not doing anything with @mentions of the bot yet
@app.event("app_mention")
def handle_app_mention_events(body, logger):
    pass

# not doing anything with reactions yet
@app.event("reaction_added")
def handle_reaction_added_events(body, logger):
    pass

# catch-all for "message" events (message_changed, message_deleted)
@app.event("message")
def handle_message_events(body, logger):
    pass

if __name__ == "__main__":
    print(f"Sitecore Community Slackbot {BOT_VERSION} starting...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
