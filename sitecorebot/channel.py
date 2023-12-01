import random
from expiring_dict import ExpiringDict

class Channel:
    def __init__(self, app, channel_info):
        self._app = app
        self._channel_info = channel_info

    @property
    def id(self) -> str:
        return self._channel_info["id"]
    
    @property
    def name(self) -> str:
        return self._channel_info["name"]

    @property
    def is_direct_messaging(self) -> bool:
        return self.is_im or self.is_mpim

    @property
    def is_channel_messaging(self) -> bool:
        return self.is_channel or self.is_group

    @property
    def num_members(self) -> int:
        return int(self._channel_info["num_members"])

    @property
    def is_im(self) -> bool:
        return bool(self._channel_info["is_im"])
    
    @property
    def is_mpim(self) -> bool:
        return bool(self._channel_info["is_mpim"])
    
    @property
    def is_channel(self) -> bool:
        return bool(self._channel_info["is_channel"])

    @property
    def is_group(self) -> bool:
        return bool(self._channel_info["is_group"])

    @property
    def is_private(self) -> bool:
        return bool(self._channel_info["is_private"])

    @property
    def topic(self) -> str:
        if self._channel_info["topic"]:
            return self._channel_info["topic"]["value"]
        return ""

    @property
    def is_archived(self) -> bool:
        return bool(self._channel_info["is_archived"])
    
    @property
    def is_member(self) -> bool:
        return bool(self._channel_info["is_member"])

### CACHING ###
cache_channels = ExpiringDict()

def get_channel(app, channel_id) -> Channel:
    if channel_id in cache_channels:
        return cache_channels[channel_id]
    else:
        try:
            channel_info = app.client.conversations_info(channel=channel_id, include_num_members=True)["channel"]
            channel = Channel(app, channel_info=channel_info)
            # Using a random expiry between 24 and 48 hours, to prevent massively spamming the Slack API all at once
            cache_channels.ttl(channel_id, channel, random.randint(86400, 86400*2))
            return channel
        except:
            print(f"ERR: Channel Not Found! ({channel_id})")
            return None
