import scipy.io.wavfile
import numpy as np

# Models
from Models.Signal import *


class Writer:

    @staticmethod
    def write(filename: str, signals: [Signal]):
        rate = 0
        data = np.array([])

        for signal in signals:
            rate = signal.rate
            data = np.append(data, signal.np_y_array())

        scipy.io.wavfile.write(filename, rate, data)
