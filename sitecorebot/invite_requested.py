# invite notification channel zInvite
invite_notification_channel = "CA6SNF4NQ"

class InviteRequest():
    def __init__(self, app, request, say):
        self._app = app
        self._incoming_request = request
        self._say = say

    @property
    def invite_request_id(self) -> str:
        return self._incoming_request["id"]

    @property
    def invite_requester_ids(self) -> [str]:
        return self._incoming_request["requester_ids"]

    @property
    def invitee_email(self) -> str:
        return self._incoming_request["email"]
    
    def deny(self):
        self._app.client.admin_inviteRequests_deny(self, invite_request_id=self.invite_request_id)

def handle_invite_requested(invite_request: InviteRequest):
    invite_request.deny()
    for uid in invite_request.invite_requester_ids:
        deny_explanation = f"Hi <@{uid}>,\n\n"
        deny_explanation += f"Your request to invite user `{invite_request.invitee_email}` to our workspace here at Sitecore Community Slack has been DENIED.\n\n"
        deny_explanation += "We require all users to go through the formal invitation process found at https://sitecore.chat to join our community. Please direct the person you want to join us to this link.\n\n"
        deny_explanation += "Kind Regards,\nYour Friendly Sitecore Community Slackbot."
        invite_request._say(text=deny_explanation, channel=uid)

        response_message = f"INVITATION REQUEST DENIED!  User <@{uid}> requested to invite user {invite_request.invitee_email}. Notification to <@{uid} has been sent."
        response_message += f"```{deny_explanation}```"
        invite_request._say(text=response_message, channel=invite_notification_channel)
