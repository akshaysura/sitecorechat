import re
from message import Message
from user import User, get_user_by_email
import sendgrid
from sendgrid import Mail, Email, To, Content

channel_sitecorebot_sandbox = "C0625KEQ2VD"
channel_sitecorebot_sandbox2 = "C062W6QCGGL"
channel_zinvite = "CA6SNF4NQ"

email_regex_pattern = "[\w\.-]+@[\w\.-]+\.\w+"

# Will be listening to "New User Request in #zinvite and #sitecorebot-sandbox"
channel_zinvite_listeners = [channel_zinvite, channel_sitecorebot_sandbox, channel_sitecorebot_sandbox2]
def new_user_request(m: Message):
    # New User Request would not happen in DMs
    if m.is_direct_message: return

    # New User Requests should only be acted on, in our defined list of channels
    if m.channel_id not in channel_zinvite_listeners: return

    match = re.search(email_regex_pattern, m.text)
    if match:
        user_request_email = match.group()
        u: User = get_user_by_email(m._app, user_request_email)

        if u:
            already_found_blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "User Already Here!",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"User was already found as <@{u.id}> ({u.name}). Use the button below to send the 'Duplicate User' email to {user_request_email}."
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "action_id": "send_existing_user_email",
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Send Email"
                            },
                            "value": f"{user_request_email}:{m.channel_id}:{m.message_ts}"
                        },
                    ]
                }
            ]

            m.react("red_circle")
            m._app.client.chat_postMessage(blocks=already_found_blocks, channel=m.channel_id, thread_ts=m.message_ts)
            print(f"{m.message_date_time_string}:New User Request:{user_request_email}:Found Existing:{u.id} ({u.name})")
        else:
            # user was not found, this is good
            m.react("large_green_circle")
            print(f"{m.message_date_time_string}:New User Request:No user found for email: {user_request_email}")

def duplicate_user_handler(m: Message, action_value: str, sendgrid_api_key: str):
    args = action_value.split(":")
    email = args[0]
    channel = args[1]
    original_message_ts = args[2]

    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    from_email = Email("noreply@sitecore.chat")
    to_email = To(email)
    subject = "Duplicate Account Requested: Sitecore Community Slack"
    content = Content("text/plain", f"Hello! \n\n" \
            "We have received an invitation request, on your behalf, for the Sitecore Community Slack. However, you already have an account, " \
            "mapped to the email address provided. The email address that we are now sending this message to. \n\n" \
            "Please note; the Sitecore Community Slack does now 'own' these accounts. Slack owns these. We cannot instigate password resets or alter them in any way. \n\n"
            "Please try logging in to Slack using this email address. If you have lost the password or require a password reset, please " \
            "follow the instructions provided in https://slack.com/help/articles/201909068-Reset-your-password \n\n" \
            "If you did not initiate this request, please reach out to one of the Sitecore Community Slack Admins. \n\n" \
            "Kind Regards, \n\n" \
            "The Sitecore Community Slack Admin Team")
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)
    if response.status_code == 202:
        print(f"DUPLICATE USER EMAIL SENT TO: {email}")
        m.respond_in_thread(f"Email sent to {email}!")
        m._app.client.chat_delete(channel=channel, ts=m.message_ts)
        m._app.client.reactions_add(channel=channel, timestamp=original_message_ts, name="email")
    else:
        error_message = f"ERROR SENDING EMAIL TO: {email}, STATUS: {response.status_code}, HEADERS: {response.headers}"
        print(error_message)
        m.respond_in_thread(error_message)
        m._app.client.reactions_add(channel=channel, timestamp=original_message_ts, name="warning")
