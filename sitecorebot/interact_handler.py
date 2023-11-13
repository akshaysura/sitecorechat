from message import Message

interact_test_channel = "C062W6QCGGL"

def interact_command(message: Message):
    interact_blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "New Interactive Message Test",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Are there mountains in Poland?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "action_id": "interact_test_response_yes",
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Oh, Absolutely!"
                    },
                    "value": f"{message.channel_id}:{message.message_ts}"
                },
                {
                    "action_id": "interact_test_response_no",
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Haha, Sitecore Slackbot made a funny 🧀"
                    },
                    "value": f"{message.channel_id}:{message.message_ts}"
                },
            ]
        }
    ]

    message.respond_to_channel(channel_id=interact_test_channel, response_message="New Interact Test Command", response_blocks=interact_blocks)
