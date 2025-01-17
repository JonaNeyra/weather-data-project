import os


class ForecastTwilioSender:
    def __init__(self, message_generator, sms_messanger):
        self.message_generator = message_generator
        self.sms_messanger = sms_messanger

    def send(self, recipient):
        msg = self.message_generator.perform()
        self.sms_messanger.make_client()
        twilio_res = self.sms_messanger.send_msg(msg, os.environ['TWILIO_PHONE_NUMBER'], recipient)

        return twilio_res
