import re
import time
from message import Message
from welcome import BOT_IMAGE_PATH
from user import bot_admins, community_coordinators

# Regex pattern to match Slack user mentions: <@U12345678>
MENTION_PATTERN = re.compile(r'<@(U[A-Z0-9]+)>')

# Additional users exempt from mention warnings (add user IDs here)
ADDITIONAL_EXEMPT_USERS = [
    # "U12345678",  # Example: Add extra user IDs who are allowed to @ mention freely
]

# Combined exempt list: admins + coordinators + any additional users
EXEMPT_USERS = bot_admins + community_coordinators + ADDITIONAL_EXEMPT_USERS

# How long (in seconds) before we remind the same user again
COOLDOWN_SECONDS = 86400  # 24 hours

# Track when users were last warned: {user_id: timestamp}
warned_users = {}

# Channel to log mention guardian activity (same as crosspost guardian)
mention_guardian_log_channel = "C0625KEQ2VD"

def mention_guardian(app, m: Message) -> bool:
    """
    Checks if a message contains @ mentions of other users.
    If so, sends an ephemeral reminder about Rule #4.
    Returns True if a warning was sent, False otherwise.
    """
    # Skip DMs, bot messages
    if m.is_direct_message or m.is_bot_message:
        return False

    # Skip if user is exempt
    if m.user.id in EXEMPT_USERS:
        return False

    # Check if user is still in cooldown period
    if m.user.id in warned_users:
        last_warned = warned_users[m.user.id]
        if time.time() - last_warned < COOLDOWN_SECONDS:
            return False

    # Find all user mentions in the message
    mentions = MENTION_PATTERN.findall(m.text)

    # Filter out self-mentions (user mentioning themselves)
    mentions = [uid for uid in mentions if uid != m.user.id]

    # If no mentions of other users, nothing to do
    if not mentions:
        return False

    # Send ephemeral warning
    try:
        app.client.chat_postEphemeral(
            channel=m.channel_id,
            user=m.user.id,
            text="Friendly reminder about tagging users",
            blocks=get_mention_warning_blocks()
        )

        # Record that we warned this user
        warned_users[m.user.id] = time.time()

        print(f"{time.ctime(time.time())}:MentionGuardian:Warned user @{m.user.name} in #{m.channel.name} for mentioning {len(mentions)} user(s)")
        return True

    except Exception as e:
        print(f"{time.ctime(time.time())}:MentionGuardian:ERROR sending ephemeral: {e}")
        return False


def get_mention_warning_blocks():
    """Returns the Slack blocks for the ephemeral warning message."""
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "👋 *Quick reminder about Rule #4!*\n\n"
                        "We noticed you tagged another user in your message. "
                        "In this community, we ask that you avoid using @ mentions to tag people directly.\n\n"
                        "*Why?* We're all volunteers here, participating in our own time. "
                        "Tagging someone can feel like putting them on the spot to respond.\n\n"
                        "Don't worry - your message is still visible and people will respond when they can! 🙂"
            },
            "accessory": {
                "type": "image",
                "image_url": BOT_IMAGE_PATH,
                "alt_text": "Sitecore Community Slackbot"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "action_id": "mention_guardian_show_rules",
                    "text": {
                        "type": "plain_text",
                        "text": "Show me all the rules",
                        "emoji": True
                    },
                    "value": "show_rules"
                }
            ]
        }
    ]


print(f"Mention Guardian Online. Exempt: {len(bot_admins)} admins, {len(community_coordinators)} coordinators, {len(ADDITIONAL_EXEMPT_USERS)} additional. Cooldown: {COOLDOWN_SECONDS}s")
