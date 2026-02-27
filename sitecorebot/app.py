BOT_VERSION = "Sitecore Community Slackbot version 0.5.0"

import os, re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from new_user_request import new_user_request, duplicate_user_handler
from crosspost_guardian import crosspost_guardian
from mention_guardian import mention_guardian
from bot_command_handler import bot_command_handler
from welcome import handle_team_join
from message import Message
from bot_memory import BotChannelMemory
from usergroup_monitor import usergroup_monitor
from url_scanner import url_scanner
from reaction_handler import reaction_handler

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
        mention_guardian(app, m)
        if not m.is_bot_message:
            print(f"{m.message_date_time_string}:#{m.channel.name}:@{m.user.name}:{m.text} [{fuzzy_score}]")
        else:
            print(f"{m.message_date_time_string}:#{m.channel.name}:@{m.username}:{m.text} [{fuzzy_score}]")
        BotChannelMemory(m.channel_id, m.channel.name, m.message_ts).start()
        url_scanner(m.text)
    else:
        print(f"{m.message_date_time_string}:{m.channel_type}:@{m.user.name}:{m.text}")
        if m.is_im:
            bot_command_handler(app, m.user.id, m.text)

# not doing anything with @mentions of the bot yet
@app.event("app_mention")
def handle_app_mention_events(body, logger):
    pass

@app.event("reaction_added")
def handle_reaction_added_events(ack, event, say):
    ack()
    if "item_user" in event and event["item"]["type"] == "message":
        reaction = event["reaction"]
        user_id = event["user"]
        item_user_id = event["item_user"]
        channel_id = event["item"]["channel"]
        message_id = event["item"]["ts"]
        reaction_handler(app, user_id, reaction, item_user_id, channel_id, message_id)

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

@app.action("mention_guardian_show_rules")
def handle_mention_guardian_show_rules(ack, body, say):
    ack()
    from welcome import display_rules
    from user import get_user
    user = get_user(app, body["user"]["id"])
    display_rules(app, user, "rules")

@app.command("/communitybot")
def handle_some_command(ack, body, say):
    ack()
    bot_command_handler(app, body["user_id"], body["text"])
    try:
        app.client.chat_postEphemeral(channel=body["channel_id"], user=body["user_id"], text="I've responded to you in an IM. Let's just keep this between the two of us 😉")
    except:
        pass

def main():
    print(f"{BOT_VERSION} starting...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()
