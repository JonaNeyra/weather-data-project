from .weather_dataframe_handler import DfRainy
from .weather_dataset_filler import WeatherDatasetFiller
from ..infrastructure.retrieve_weather import weather_res
from ..templates.twilio_tmp import MESSAGE_TWILIO


class GenerateForecastMessageFrom:
    def __init__(self, location):
        self.location = location
        self.data = None
        self.df = None

    def perform(self):
        res = weather_res(self.location.name)
        self.weather_dataset(res)
        result = self.rainy_dataset()
        msg = self.twilio_msg(result)

        return msg

    def twilio_msg(self, result):
        return MESSAGE_TWILIO.format(
            date=self.df['Fecha'][0],
            location=self.location.name,
            dataframe=str(result),
        )

    def rainy_dataset(self):
        df_rainy = DfRainy(self.data)
        df_rainy.create()
        self.df = df_rainy.df

        return df_rainy.filter()

    def weather_dataset(self, res):
        wdf = WeatherDatasetFiller(res)
        self.data = wdf.fill()
