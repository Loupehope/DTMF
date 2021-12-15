import numpy as np


class Signal:
    # Класс определеяет один DTMF-сигнал.
    #
    # Properties
    # ----------
    # data : путь к файлу.
    # symbol : символ DTMF-сигнала.
    # rate : частота дискретизации.

    # Initialization
    def __init__(self, data, symbol, rate):
        self.y_array = data[1]
        self.symbol = symbol
        self.rate = rate

    def np_y_array(self):
        # Преобразует данные в numpy array.
        #
        # Returns
        # -------
        # data : numpy array
        #     Данные файла.

        return np.array(self.y_array)
