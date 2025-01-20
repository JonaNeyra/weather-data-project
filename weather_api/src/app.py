import os

from dotenv import load_dotenv

from send_forecast.app.send_forecast_use_case import SendForecastUseCase
from send_forecast.domain.service_entities import Recipient, Location
from send_forecast.infrastructure.sms_twilio_messanger import SMSTwilioMessanger
from send_forecast.services.forecast_twlio_sender import ForecastTwilioSender
from send_forecast.services.generate_forecast_message_from import GenerateForecastMessageFrom

load_dotenv()

if __name__ == "__main__":
    location = Location("Noruega")
    sender = ForecastTwilioSender(
        message_generator=GenerateForecastMessageFrom(location),
        sms_messanger=SMSTwilioMessanger(
            os.environ['TWILIO_ACCOUNT_SID'],
            os.environ['TWILIO_AUTH_TOKEN']
        )
    )
    recipient = Recipient(os.environ['TO_PHONE_NUMBER'])

    use_case = SendForecastUseCase(sender, recipient)
    res = use_case.execute()

    print(res.sid)
