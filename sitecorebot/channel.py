
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

### CACHING ###

cache_channels = {}

def get_channel(app, channel_id) -> Channel:
    if channel_id in cache_channels:
        return cache_channels[channel_id]
    else:
        try:
            channel_info = app.client.conversations_info(channel=channel_id, include_num_members=True)["channel"]
            channel = Channel(app, channel_info=channel_info)
            cache_channels[channel_id] = channel
            return channel
        except:
            return None
