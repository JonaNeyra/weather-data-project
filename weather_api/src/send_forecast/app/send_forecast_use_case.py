class SendForecastUseCase:
    def __init__(self, sender, recipient):
        self.sender = sender
        self.recipient = recipient

    def execute(self):
        return self.sender.send(self.recipient.phone)
