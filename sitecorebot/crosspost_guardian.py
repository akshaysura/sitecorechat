from thefuzz import fuzz
from message import Message

FUZZY_RATIO_THRESHOLD = 90      # Lower means bigger risk of false positives
MESSAGE_LENGTH_THRESHOLD = 20   # messages shorter than this will be ignored by the crosspost guardian

user_message_memory = {}

crosspost_guardian_alert_channel = "C0625KEQ2VD"

def crosspost_guardian(m: Message) -> int:
    # We shouldn't get called for DMs, but just in case. Bot messages (RSS feed etc) are also ignored.
    if m.is_direct_message or m.is_bot_message: return 0

    # ignore short messages to avoid false positives on "ok", "right", "nice", "boot", ":smile:", and so on.
    if len(m.text) < MESSAGE_LENGTH_THRESHOLD: return 0

    if m.user.id == "U05GHTMUNTH": return 0 # Slackbot, which for some reason doesn't register as a bot_message
    
    if m.user.id in user_message_memory:
        message_list = user_message_memory[m.user.id]

        highest_fuzzy_score = 0
        suspected_duplicate = None

        for previous_message in message_list:
            # To work around Slack notifying us about the same message twice, for whatever reason. Crossposts aren't cross if they happen in same channel
            if m.channel_id == previous_message.channel_id:
                continue

            fuzzy_ratio = fuzz.ratio(m.text, previous_message.text)
            highest_fuzzy_score = max(highest_fuzzy_score, fuzzy_ratio)

            if fuzzy_ratio > FUZZY_RATIO_THRESHOLD:
                # Check to make sure the suspected duplicate original message is still around
                if previous_message.get_permalink():
                    suspected_duplicate = previous_message
                    break

        if suspected_duplicate:
            message_text =  f"Message {m.get_permalink()} in channel <#{m.channel_id}> " \
                            f"is a suspected duplicate of {suspected_duplicate.get_permalink()} in channel <#{suspected_duplicate.channel_id}>. " \
                            f"Confidence: {highest_fuzzy_score}"
            m.respond_to_channel(crosspost_guardian_alert_channel, message_text)

        message_list.insert(0, m)
        message_list = message_list[:5] # only keep most recent 5 messages in memory per user

        return highest_fuzzy_score
    else:
        user_message_memory[m.user.id] = [m]
        return 0

print(f"Crosspost Guardian Online. Target Channel: {crosspost_guardian_alert_channel}. Fuzzy Threshold: {FUZZY_RATIO_THRESHOLD}. Message Length Threshold: {MESSAGE_LENGTH_THRESHOLD}")
