from thefuzz import fuzz
from defs import channel_sitecorebot_sandbox

user_message_memory = {}

def crosspost_guardian(app, message, say) -> int:
    user_id = message["user"]
    channel_id = message["channel"]
    message_ts = message["ts"]

    # We shouldn't get called for DMs, but just in case
    channel_type = message["channel_type"]
    if channel_type == "im":
        return 0

    # ignore short messages to avoid false positives on "ok", "right", "nice", "boot", ":smile:", and so on.
    message_text = message["text"]
    if len(message_text) < 20:
        return 0
    
    if user_id in user_message_memory:
        message_list = user_message_memory[user_id]

        highest_fuzzy_score = 0
        incoming_message_text = message["text"]
        suspected_duplicate = None

        for m in message_list:
            # add a message obsolecense here, like if the message is more than 1 hour old, disregard. Maybe. To discuss.

            fuzzy_ratio = fuzz.ratio(incoming_message_text, m["text"])
            if fuzzy_ratio > 90:
                suspected_duplicate = m

            highest_fuzzy_score = max(highest_fuzzy_score, fuzzy_ratio)

        if not suspected_duplicate is None:
            message_permalink = app.client.chat_getPermalink(channel=channel_id, message_ts=message_ts)
            message_channel = app.client.conversations_info(channel=channel_id, include_num_members=False)["channel"]
            duplicate_suspect_permalink = app.client.chat_getPermalink(channel=suspected_duplicate["channel"], message_ts=suspected_duplicate["ts"])
            duplicate_suspect_channel = app.client.conversations_info(channel=suspected_duplicate["channel"], include_num_members=False)["channel"]
            message_text =  f"Message {message_permalink['permalink']} in channel #{message_channel['name']} " \
                            f"is a suspected duplicate of {duplicate_suspect_permalink['permalink']} in channel #{duplicate_suspect_channel['name']}. " \
                            f"Confidence: {highest_fuzzy_score}"
            app.client.chat_postMessage(channel=channel_sitecorebot_sandbox, text=message_text)

        message_list.insert(0, message)
        message_list = message_list[:5] # only keep most recent 5 messages in memory per user

        return highest_fuzzy_score
    else:
        print(f"Initialised message memory for {user_id}")
        user_message_memory[user_id] = [message]
        return 0
