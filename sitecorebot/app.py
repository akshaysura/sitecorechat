from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def app_mention_handler(body, say):
    say("Poland has mountains!")

@app.message("mountains")
def app_mention_mountains(message, say):
    say(text=f"You know <@{message['user']}>, Poland has mountains too!")

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
