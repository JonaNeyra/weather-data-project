class ForecastHourly:
    def __init__(self, date, hour, condition, temp_c, will_it_rain, chance_of_rain):
        self.date = date
        self.hour =hour
        self.condition = condition
        self.temp_c = temp_c
        self.will_it_rain = will_it_rain
        self.chance_of_rain =chance_of_rain

    def __iter__(self):
        yield self.date
        yield self.hour
        yield self.condition
        yield self.temp_c
        yield self.will_it_rain
        yield self.chance_of_rain
