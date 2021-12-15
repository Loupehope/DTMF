from Processing.Goertzel import *


class Detector:

    @staticmethod
    def detect(rate, data) -> str:
        # Декодирует wav файл.
        #
        # Parameters
        # ----------
        # rate : путь к файлу.
        # data : данные сигнала.
        #
        # Returns
        # -------
        # result : str
        #     декодированная строка сигнала.

        result = ""
        bin_size = int(rate * .25)
        goertzel = Goertzel(rate, bin_size)

        for i in range(0, len(data) - bin_size + 1, bin_size):
            goertzel.reset()

            for j in range(bin_size):
                goertzel.calc_s_n(data[i + j])

            powers = goertzel.calc_power()
            symbol = goertzel.get_number(powers)

            result += symbol

        return result
