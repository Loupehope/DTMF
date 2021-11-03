import numpy as np


class Signal:

    # Initialization
    def __init__(self, data, symbol, rate):
        self.x_array = data[0]
        self.y_array = data[1]
        self.symbol = symbol
        self.rate = rate

    def np_y_array(self):
        return np.array(self.y_array)