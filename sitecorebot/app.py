BOT_VERSION = "Sitecore Community Slackbot version 0.4.6"

import os, re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from new_user_request import new_user_request, duplicate_user_handler
from hey_sitecorebot import hey_sitecorebot
from crosspost_guardian import crosspost_guardian
from bot_command_handler import bot_command_handler
from welcome import handle_team_join
from message import Message
from bot_memory import BotChannelMemory
from usergroup_monitor import usergroup_monitor
from url_scanner import url_scanner

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

app = App(token=SLACK_BOT_TOKEN)

@app.message("New User Request")
def app_new_user_request(message, say):
    m: Message = Message(app, message, say)
    new_user_request(m)

@app.event("team_join")
def handle_team_join_events(event, say):
    user_id = event["user"]["id"]
    handle_team_join(app, say, user_id)

@app.event("invite_requested")
def handle_invite_requested_events(event, say):
    from invite_requested import InviteRequest, handle_invite_requested
    print(f"INVITE REQUESTED: {event}")
    ir: InviteRequest = InviteRequest(app, event["invite_request"], say)
    handle_invite_requested(ir)

@app.message(re.compile("([hH]ey|[hH]ello) [sS]itecore[bB]ot"))
def app_hey_sitecorebot(message, say):
    m: Message = Message(app, message, say)
    hey_sitecorebot(m)

@app.message(re.compile("(sugbce.in|zoom.us|webex.com|meetup.com)"))
def app_usergroup_monitor(message, say):
    m: Message = Message(app, message, say)
    if m.is_channel_message:
        BotChannelMemory(m.channel_id, m.channel.name, m.message_ts).start()
    usergroup_monitor(m)

@app.message(re.compile("^."))
def all_message_handler(message, say):
    m: Message = Message(app, message, say)

    if m.is_channel_message:
        fuzzy_score = crosspost_guardian(m)
        if not m.is_bot_message:
            print(f"{m.message_date_time_string}:#{m.channel.name}:@{m.user.name}:{m.text} [{fuzzy_score}]")
        else:
            print(f"{m.message_date_time_string}:#{m.channel.name}:@{m.username}:{m.text} [{fuzzy_score}]")
        BotChannelMemory(m.channel_id, m.channel.name, m.message_ts).start()
        url_scanner(m.text)
    else:
        print(f"{m.message_date_time_string}:{m.channel_type}:@{m.user.name}:{m.text}")
        bot_command_handler(m)

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
def handle_message_events(event, say):
    pass
#    print(f"EVENT: {event}")

@app.event("hello")
def handle_hello_events(body, logger):
    print("Slack API said hello!")

@app.action("send_existing_user_email")
def handle_duplicate_user_action(ack, body, say):
    ack()
    m: Message = Message(app, body["message"], say)
    action_value = body["actions"][0]["value"]
    duplicate_user_handler(m, action_value, SENDGRID_API_KEY)

@app.command("/communitybot")
def handle_some_command(ack, body):
    ack()
    print(f"COMMAND: {body}")

def main():
    print(f"{BOT_VERSION} starting...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()
