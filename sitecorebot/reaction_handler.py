import copy
from slack_bolt import App
from message import Message, get_message_permalink
from user import User, get_user, is_bot_admin_user, is_community_coordinator
from channel import Channel, get_channel

SNIPPETS_IMAGE_PATH = "https://sitecore.chat/images/snippets.png"
REACTION_COUNT_THRESHOLD = 3
CARBON_COPY_CHANNEL = "C0625KEQ2VD"

reaction_memory = []

def reaction_handler(app: App, user_id, reaction, item_user_id, channel_id, message_id):
    # drop out immediately if we've already acted on this message
    umid = channel_id+message_id
    if umid in reaction_memory:
        return

    reacting_user = get_user(app, user_id)
    message_user = get_user(app, item_user_id)
    channel = get_channel(app, channel_id)
    print(f"User: {reacting_user.name} is reacting with :{reaction}: to {message_user.name}'s message in channel: {channel.name}")
    
    handler = get_reaction_handler(reaction)
    if handler:
        react_now = is_bot_admin_user(user_id) or is_community_coordinator(user_id)
        if not react_now:
            # if not reacting right away, figure out if enough users have reacted to warrant going ahead anyway
            count = get_reaction_count(app, channel_id, message_id, reaction)
            if count >= REACTION_COUNT_THRESHOLD:
                react_now = True

        if react_now:
            handler(app, user_id, item_user_id, channel_id, message_id)
            reaction_memory.append(umid)
        else:
            try:
                app.client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"Your reaction :{reaction}: has been recorded. If {REACTION_COUNT_THRESHOLD} or more users " \
                                              f"react in the same way, <@{item_user_id}> will be notified in a DM with an explanatory text and guide, on how to amend their post.")
            except:
                pass

def snippets_handler(app: App, user_id, item_user_id, channel_id, message_id):
    message_user = get_user(app, item_user_id)
    app.client.chat_postMessage(channel=item_user_id, text="Snippets Instruction!", attachments=snippets_attachments, blocks=block_replacer(app, snippets_blocks, channel_id, message_id))
    print(f":snippets: explanatory text sent to user: @{message_user.name}")
    r = app.client.chat_postMessage(channel=CARBON_COPY_CHANNEL, text=f":snippets: Reaction Handled, Snippets instruction text sent to user <@{item_user_id}>. Below is what was sent.")
    app.client.chat_postMessage(channel=CARBON_COPY_CHANNEL, thread_ts=r["ts"], text="Snippets Instruction!", attachments=snippets_attachments, blocks=block_replacer(app, snippets_blocks, channel_id, message_id))
    app.client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"Thank you. The user has been sent friendly guidance on the use of Snippets in Slack!")

reactions = {
    "snippets": snippets_handler,
}

def get_reaction_count(app: App, channel_id, message_ts, reaction) -> int:
    reactions_get = app.client.reactions_get(channel=channel_id, timestamp=message_ts)
    reactions = reactions_get["message"]["reactions"]
    if reactions:
        reaction = next(n for n in reactions if n["name"] == reaction)
        if reaction:
            return int(reaction["count"])
    return 0

def get_reaction_handler(reaction: str) -> callable:
    if reaction in reactions:
        return reactions[reaction]
    return None

def block_replacer(app: App, input, channel_id, message_id):
    output = copy.deepcopy(input)
    for n in output:
        if n["text"]["text"]:
            n["text"]["text"] = n["text"]["text"].replace("#MESS#", get_message_permalink(app, channel_id, message_id))
    return output

snippets_blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "An introduction to Snippets!",
            "emoji": True,
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hey there 🙂 \n\nI'm the Sitecore Community Slackbot!\n\n" \
                "I'm writing to you in regards to your message #MESS#. \n\n " \
                "Don't worry, nothing bad going on. But your message has been flagged with :snippets: and I'm here to explain to you, what that means 🙂 \n\n" \
                "Basically, if you're pasting large amounts of text into a message - like a stack trace or something similar, the community REALLY " \
                "prefers it if you use the 'snippets' functionality in Slack. This makes for a MUCH better reading experience overall, but also massively " \
                "improves the experience for our users on mobile devices and tablets. \n\n" \
                "Please see this attached illustration of how to create snippets, and edit your message accordingly. Thanks in advance 🙂 \n\n"
        },
        "accessory": {
            "type": "image",
            "image_url": SNIPPETS_IMAGE_PATH,
            "alt_text": "How to create Snippets in Slack"
        }
    },
]

snippets_attachments = [
    {
        "title": "How to use Snippets!",
        "image_url": SNIPPETS_IMAGE_PATH,
    }
]