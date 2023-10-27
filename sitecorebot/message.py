import time
from user import User, get_user
from channel import Channel, get_channel

class Message:
    def __init__(self, app, message, say):
        self._app = app
        self._message = message
        self._user = None
        self._channel = None
        self._say = say

    @property
    def is_direct_message(self) -> bool:
        return self._message["channel_type"] in ["im", "mpim"]
    
    @property
    def is_channel_message(self) -> bool:
        return self._message["channel_type"] not in ["im", "mpim"]

    @property
    def text(self) -> str:
        return self._message["text"]

    @property
    def channel_id(self) -> str:
        return self._message["channel"]
    
    @property
    def message_ts(self) -> str:
        return self._message["ts"]

    @property
    def message_date_time_string(self) -> str:
        return time.ctime(float(self.message_ts))

    @property
    def user(self) -> User:
        if not self._user:
            self._user = get_user(self._app, self._message["user"])
        return self._user

    @property
    def channel(self) -> Channel:
        if not self._channel:
            self._channel = get_channel(self._app, self._message["channel"])
        return self._channel

    def get_permalink(self):
        return self._app.client.chat_getPermalink(channel=self.channel_id, message_ts=self.message_ts)["permalink"]

    def react(self, emoji="thumbsup"):
        self._app.client.reactions_add(channel=self.channel_id, timestamp=self.message_ts, name=emoji)
    
    def respond_in_thread(self, response_message):
        self._say(text=response_message, thread_ts=self.message_ts)

    def respond(self, response_message):
        self._say(text=response_message, channel=self._message["channel"])

    def respond_to_channel(self, channel_id, response_message):
        self._app.client.chat_postMessage(channel=channel_id, text=response_message)
