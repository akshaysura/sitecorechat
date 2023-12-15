import time
from user import User, get_user

BOT_IMAGE_PATH = "https://sitecore.chat/images/slackbot-profile-256x256.png"
WELCOME_CHANNEL_ID = "C06A9HY37B4"

def handle_team_join(app, say, user_id):
    u: User = get_user(app, user_id)
    if not u:
        print(f"{time.ctime(time.time())}:ERROR: TEAM JOIN EVENT, USER NOT FOUND: {user_id}")
        return

    response_message = f"New User: <@{u.id}> ({u.real_name}) joined our community 🥳"
    say(channel=user_id, text="Welcome Message", blocks=header_blocks)
    say(channel=user_id, text="Divider1", blocks=divider_blocks)
    say(channel=user_id, text="Rules", blocks=rules_overview_blocks)
    say(channel=user_id, text="Divider2", blocks=divider_blocks)
    say(channel=user_id, text="Footer", blocks=footer_blocks)
    print(f"{time.ctime(time.time())}:NEW USER JOINED: {response_message}")

    say(text=response_message, channel=WELCOME_CHANNEL_ID)
    return

def display_welcome(app, user, command_text):
    user.send_im_message("Welcome Response", header_blocks)
    user.send_im_message("Divider1", divider_blocks)
    user.send_im_message("Rules", rules_overview_blocks)
    user.send_im_message("Divider2", divider_blocks)
    user.send_im_message("Footer", footer_blocks)

def display_rules(app, user, command_text):
    user.send_im_message("Rules", rules_blocks)

divider_blocks = [
    {
        "type": "divider"
    },
]

header_blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Welcome to the Sitecore Community Slack!",
            "emoji": True,
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hi there, and welcome 🙂 \n\nI'm the Sitecore Community Slackbot!\n\n" \
                "Think of me as sort of an online concierge, I'm here to help you get an " \
                "overview of this global Sitecore Community counting almost 10.000 members as of today. \n\n" \
                "We're a pretty big community. Every week almost 5.000 messages are shared here, either in one of our many public channels or in private conversations between our members. \n\n" \
                "As you can imagine, with this many people and this many messages, we have a few basic rules and guidelines in place, that help keep this community " \
                "a nice place to be that has people coming back day after day. \n\n" \
                "Don't worry, it's all very simple! \n\n"
        },
        "accessory": {
            "type": "image",
            "image_url": BOT_IMAGE_PATH,
            "alt_text": "Sitecore Community Slackbot Profile Image"
        }
    },
]

footer_blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "And with that out of the way, welcome!",
            "emoji": True,
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": 
                "The last thing I need to tell you about, is...  me. As any proper concierge, I can help you in various ways. I can respond to private messages you send me. " \
                "For instance, if you type `help` below, I will send you a list of the commands I currently have available for you. \n\n" \
                "Or you can type `rules` at any time, if you want a repeat of the current rules and guidelines of this Sitecore Community Slack. \n\n " \
                "For feedback, you can provide (anonymous) feedback using the `feedback` command. \n\n " \
                "Lastly, to get the list of community members currently managing this Sitecore Community Slack, type `admins`."
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Best Regards, \n\n The Sitecore Community"
        },
        "accessory": {
            "type": "image",
            "image_url": BOT_IMAGE_PATH,
            "alt_text": "Sitecore Community Slackbot Profile Image"
        }
    },
]

rules_overview_blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Rules (summary) for this Sitecore Community Slack!",
            "emoji": True,
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "For a full explanation of these rules, please respond to this message by typing `rules` below."
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "1️⃣ - Engage and Share. Like every good community, we work on a 'give and take' basis. \n" \
                "2️⃣ - Check the Sitecore Stack Exchange https://sitecore.stackexchange.com before asking. \n" \
                "3️⃣ - Please don't cross-post the same question in multiple channels. \n" \
                "4️⃣ - Don't tag people (using @ <user name>). We're a community of volunteers. \n" \
                "5️⃣ - Keep on topic. We're discussing Sitecore (company and products) in this community."
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Don't worry! As you will quickly find, we're a very relaxed community. The rules and guidelines we have in place are there " \
                "for the benefit of everyone. For a more in-depth explanation behind the above rules, get the full explanation by responding `rules` to this message."
        }
    },
]

rules_blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Rules of the Sitecore Community Slack!",
            "emoji": True,
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "1️⃣ Engage and share. \n\n We're a community centered around the Sitecore products, sharing our knowledge, asking questions, sharing experiences (good or bad), " \
                "helping people out. The value of this community comes from the amount of effort our members put into it. \n\n" \
                "This is to say; feel free to ask questions. But try to also find time to answer questions in here when you can."
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "2️⃣ Check the Sitecore Stack Exchange. \n\n The Sitecore Community also runs the https://sitecore.stackexchange.com knowledge database. \n\n" \
                "Before asking a question, it is always a good idea to see if the question you have has already been recorded and answered there. \n\n " \
                "This Slack Community has no 'memory', so if you think your question (and solution) will be valuable for everyone, please consider sharing it there for everyone to enjoy."
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "3️⃣ Please don't cross-post. \n\n While we certainly understand, you have a burning question that desperately needs an answer right away, " \
                "posting the question in multiple different channels is NOT the right way to go about it. \n\n" \
                "Questions almost always turn into conversations. Conversations where follow-up or clarifying questions are asked, additional details shared, and so on. \n\n" \
                "This can't take place, if you have two or more separate conversations going about the same question. Or worse; a friendly community member might choose to " \
                "invest their time (see point 1️⃣ above) and try and help you out. Only to then find that important context has already been provided in your duplicate conversation. \n\n" \
                "In short; don't do it 🙂. Please!"
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "4️⃣ Don't tag people. \n\n In short, we're all here on our own time. We're a community of volunteers, and we all have many different things " \
                "going on throughout our day. While it might seem tempting to just tag @ <some user> because you know they will likely have the answer you seek, " \
                "please don't do it. \n\n " \
                "As an extension of this, don't DM people directly with questions unless you have already agreed this in advance. Once again; we're a community of " \
                "volunteers, no one here is paid to act as support engineers or on-demand encyclopedias 😉. \n\n" \
                "If you do have an urgent issue, take it to the official Sitecore Support site or perhaps take a look at https://sitecore.stackexchange.com to see if " \
                    "your question already has an answer on record there."
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "5️⃣ Keep on topic. \n\n This Sitecore Community Slack is about... Sitecore. The company and their products and related (sometimes competing) products. \n\n" \
                "We're a global and very diverse community, and while we certainly realise that there's a lot more to people and their lives than 'just Sitecore', " \
                "'just Sitecore' is what this Slack is about. This is not the place to discuss current events, politics, religion, or whatever else might be on your mind. \n\n" \
                "There are a few exceptions. From time to time a few subcommunities have formed here (#gaming, as an example). Generally speaking however, in here 'we talk Sitecore'."
        }
    },
]

print("New User Joined monitor is online!")
