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
    def is_bot_message(self) -> bool:
        if self._message.get("subtype") is None: return False
        return self._message["subtype"] == "bot_message"

    @property
    def is_im(self) -> bool:
        return self._message["channel_type"] == "im"

    @property
    def is_mpim(self) -> bool:
        return self._message["channel_type"] == "mpim"

    @property
    def is_channel_message(self) -> bool:
        return self._message["channel_type"] not in ["im", "mpim"]

    @property
    def text(self) -> str:
        return self._message["text"]

    @property
    def channel_id(self) -> str:
        return self._message["channel"]
    
    # set for bot messages
    @property
    def username(self) -> str:
        return self._message["username"]
    
    @property
    def message_ts(self) -> str:
        return self._message["ts"]

    @property
    def message_date_time_string(self) -> str:
        return time.ctime(float(self.message_ts))

    @property
    def user(self) -> User:
        if not self._user:
            try:
                self._user = get_user(self._app, self._message["user"])
            except:
                print(f"ERROR. No 'user' information present on message: {self._message}")
        return self._user

    @property
    def channel_type(self) -> str:
        return self._message["channel_type"]
    
    @property
    def channel(self) -> Channel:
        if not self._channel:
            try:
                self._channel = get_channel(self._app, self._message["channel"])
            except:
                print(f"ERROR. No 'channel' information present on message: {self._message}")
        return self._channel

    def get_permalink(self):
        try:
            return self._app.client.chat_getPermalink(channel=self.channel_id, message_ts=self.message_ts)["permalink"]
        except:
            return None

    def react(self, emoji="thumbsup"):
        self._app.client.reactions_add(channel=self.channel_id, timestamp=self.message_ts, name=emoji)
    
    def respond_in_thread(self, response_message, response_blocks=None):
        self._say(text=response_message, thread_ts=self.message_ts, response=response_blocks)

    def respond(self, response_message, response_blocks=None):
        self._say(text=response_message, channel=self._message["channel"], blocks=response_blocks)

    def respond_to_channel(self, channel_id, response_message, response_blocks=None):
        self._app.client.chat_postMessage(channel=channel_id, text=response_message, blocks=response_blocks)
