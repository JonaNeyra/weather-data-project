from tqdm import tqdm

from ..domain import entities


class WeatherDatasetFiller:
    def __init__(self, weather):
        self.weather = weather
        self.forecast_data = self.weather['forecast']['forecastday'][0]['hour']

    def fill(self):
        data = []
        for hour in tqdm(range(0, 24), colour='#7a00bd'):
            forecast_obj = self.retrieve_forecast_hours(hour_pos=hour)
            data.append(tuple(forecast_obj))

        return data

    def retrieve_forecast_hours(self, hour_pos):
        return entities.ForecastHourly(
            date=self.forecast_data[hour_pos]['time'].split()[0],
            hour=int(self.forecast_data[hour_pos]['time'].split()[1].split(':')[0]),
            condition=self.forecast_data[hour_pos]['condition']['text'],
            temp_c=self.forecast_data[hour_pos]['temp_c'],
            will_it_rain=self.forecast_data[hour_pos]['will_it_rain'],
            chance_of_rain=self.forecast_data[hour_pos]['chance_of_rain'],
        )
