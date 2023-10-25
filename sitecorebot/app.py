import os, re, time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

bot_admins = ["U0D8XHJSH", "U09SJ4FGW"]
channel_zinvite = ["CA6SNF4NQ", "C0625KEQ2VD"]

email_regex_pattern = "[\w\.-]+@[\w\.-]+\.\w+"

@app.message("New User Request")
def app_new_user_request(message, say):
    channel_id = message["channel"]
    message_text = message["text"]
    message_ts = message["ts"]

    if channel_id not in channel_zinvite:
        print(f"New User Request ignored in channel {channel_id}")
        return

    match = re.search(email_regex_pattern, message_text)
    if match:
        user_request_email = match.group()
        print(f"Incoming New User Request for Email {user_request_email}")
        try:
            userinfo_request = app.client.users_lookupByEmail(email=user_request_email)
            existing_userinfo = userinfo_request["user"]
            app.client.reactions_add(channel=channel_id, timestamp=message["ts"], name="red_circle")
            response_message = f"Found user as <@{existing_userinfo['id']}> ({existing_userinfo['real_name']})"
            say(text=response_message, thread_ts=message_ts)
            say(text = f"```{existing_userinfo}```", thread_ts=message_ts)
            print(response_message)
        except:
            # user was not found, this is good
            app.client.reactions_add(channel=channel_id, timestamp=message["ts"], name="large_green_circle")
            print("This is a new user")

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

# catch-all
@app.event("message")
def handle_message_events(body, logger):
    print(body)

# not doing anything with @mentions of the bot yet
@app.event("app_mention")
def handle_app_mention_events(body, logger):
    print(body)

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
