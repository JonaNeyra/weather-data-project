import pandas as pd

class DfRainy:
    DF_RAINY_COLS: list[str] = ['Fecha', 'Hora', 'Condición', 'Temperatura', 'Lluvia', 'Probabilidad de Lluvia']

    def __init__(self, data):
        self.data = data
        self.cols = self.DF_RAINY_COLS
        self.df = None

    def create(self):
        self.df = pd.DataFrame(self.data, columns=self.cols)

    def filter(self):
        df_rainy = self.df[(self.df['Lluvia'] == 1) & (self.df['Hora'] > 6) & (self.df['Hora'] < 22)]
        df_rainy = df_rainy[['Hora', 'Condición']]
        df_rainy.set_index('Hora', inplace=True)
        return df_rainy
