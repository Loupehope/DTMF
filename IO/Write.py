import scipy.io.wavfile

# Models
from Models.Signal import *


class Writer:

    @staticmethod
    def write(filename: str, signals: [Signal]):
        # Записывает данные в wav файл.
        #
        # Parameters
        # ----------
        # filename : путь к файлу.
        # signals : массив закодированных DTMF-сигналов.

        rate = 0
        data = np.array([])

        for signal in signals:
            rate = signal.rate
            data = np.append(data, signal.np_y_array())

        scipy.io.wavfile.write(filename, rate, data)
