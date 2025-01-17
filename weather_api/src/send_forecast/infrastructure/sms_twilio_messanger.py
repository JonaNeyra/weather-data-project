from twilio.rest import Client

class SMSTwilioMessanger:
    def __init__(self, account_sid, auth_token):
        self.account_sid =account_sid
        self.auth_token = auth_token
        self.client = None

    def make_client(self):
        self.client = Client(self.account_sid, self.auth_token)

    def send_msg(self, body, _from, _to):
        msg = self.client.messages.create(
            body=body,
            from_=_from,
            to=_to
        )

        return msg
