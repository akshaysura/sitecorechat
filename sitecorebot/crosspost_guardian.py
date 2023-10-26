from thefuzz import fuzz
from user import User, get_user
from channel import Channel, get_channel

FUZZY_RATIO_THRESHOLD = 90      # Lower means bigger risk of false positives
MESSAGE_LENGTH_THRESHOLD = 20   # messages shorter than this will be ignored by the crosspost guardian

user_message_memory = {}

crosspost_guardian_alert_channel = "C0625KEQ2VD"

def crosspost_guardian(app, message, say) -> int:
    user: User = get_user(app, message["user"])
    channel: Channel = get_channel(app, message["channel"])

    # We shouldn't get called for DMs, but just in case
    if channel.is_direct_messaging:
        return 0

    message_ts = message["ts"]

    # ignore short messages to avoid false positives on "ok", "right", "nice", "boot", ":smile:", and so on.
    message_text = message["text"]
    if len(message_text) < MESSAGE_LENGTH_THRESHOLD:
        return 0
    
    if user.id in user_message_memory:
        message_list = user_message_memory[user.id]

        highest_fuzzy_score = 0
        incoming_message_text = message["text"]
        suspected_duplicate = None

        for m in message_list:
            # add a message obsolecense here, like if the message is more than 1 hour old, disregard. Maybe. To discuss.

            fuzzy_ratio = fuzz.ratio(incoming_message_text, m["text"])
            if fuzzy_ratio > FUZZY_RATIO_THRESHOLD:
                suspected_duplicate = m

            highest_fuzzy_score = max(highest_fuzzy_score, fuzzy_ratio)

        if not suspected_duplicate is None:
            message_permalink = app.client.chat_getPermalink(channel=channel.id, message_ts=message_ts)
            message_channel = app.client.conversations_info(channel=channel.id, include_num_members=False)["channel"]
            duplicate_suspect_permalink = app.client.chat_getPermalink(channel=suspected_duplicate["channel"], message_ts=suspected_duplicate["ts"])
            duplicate_suspect_channel = app.client.conversations_info(channel=suspected_duplicate["channel"], include_num_members=False)["channel"]
            message_text =  f"Message {message_permalink['permalink']} in channel #{message_channel['name']} " \
                            f"is a suspected duplicate of {duplicate_suspect_permalink['permalink']} in channel #{duplicate_suspect_channel['name']}. " \
                            f"Confidence: {highest_fuzzy_score}"
            app.client.chat_postMessage(channel=crosspost_guardian_alert_channel, text=message_text)

        message_list.insert(0, message)
        message_list = message_list[:5] # only keep most recent 5 messages in memory per user

        return highest_fuzzy_score
    else:
        user_message_memory[user.id] = [message]
        return 0
