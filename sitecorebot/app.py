import os, re, time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

channel_sitecorebot_sandbox = "C0625KEQ2VD"
channel_zinvite = "CA6SNF4NQ"
user_cassidydotdk = "U0D8XHJSH"
user_akshaysura = "U09SJ4FGW"
user_sitecorejunkie = "U09SJGX5X"

# No special priveleges implemented for admins yet
bot_admins = [user_cassidydotdk, user_akshaysura]
# Will be listening to "New User Request in #zinvite and #sitecorebot-sandbox"
channel_zinvite = [channel_zinvite, channel_sitecorebot_sandbox]

email_regex_pattern = "[\w\.-]+@[\w\.-]+\.\w+"

@app.message("New User Request")
def app_new_user_request(message, say):
    channel_id = message["channel"]
    message_text = message["text"]
    message_ts = message["ts"]

    if channel_id not in channel_zinvite:
        channel = app.client.conversations_info(channel=channel_id, include_num_members=True)["channel"]
        ignored_message = f"New User Request ignored in channel {channel['name']} ({channel_id})"
        app.logger.debug(ignored_message)
        print(ignored_message)
        return

    match = re.search(email_regex_pattern, message_text)
    if match:
        user_request_email = match.group()
        print(f"Incoming New User Request for Email {user_request_email}")
        try:
            userinfo_request = app.client.users_lookupByEmail(email=user_request_email)
            existing_userinfo = userinfo_request["user"]
            app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="red_circle")
            response_message = f"Found user as <@{existing_userinfo['id']}> ({existing_userinfo['real_name']})"
            say(text=response_message, thread_ts=message_ts)
            say(text = f"```{existing_userinfo}```", thread_ts=message_ts)
            print(response_message)
        except:
            # user was not found, this is good
            app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="large_green_circle")
            print(f"Incoming request for {user_request_email} is a new user")

# reference message pattern implementation
@app.message(re.compile("([hH]ey|[hH]ello) [sS]itecore[bB]ot"))
def app_sitecorebot_referred(message, say):
    channel_id = message["channel"]
    message_ts = message["ts"]

    if message["user"] not in bot_admins:
        app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="thumbsdown")
    else:
        app.client.reactions_add(channel=channel_id, timestamp=message_ts, name="thumbsup")

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
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
