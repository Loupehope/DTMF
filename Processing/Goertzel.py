import math

from Helpers.Const import *


class Goertzel:
    # Реализация алгоритма Герцеля.

    def __init__(self, sample_rate: int, bin_size: int):
        self.s_prev = {}
        self.s_prev2 = {}
        self.coeff = {}

        for k in DTMF_FREQ:
            self.s_prev[k] = .0
            self.s_prev2[k] = .0

            freq_k = .5 + (bin_size * k) / sample_rate

            self.coeff[k] = 2.0 * math.cos(2.0 * math.pi * freq_k / bin_size)

    def get_number(self, powers):
        # Возвращает символ соответствующий
        # полученным частотных компонентам.
        #
        # Parameters
        # ----------
        # powers : магнитуды частот.
        #
        # Returns
        # -------
        # key : str
        #     декодированный DTMF-символ.

        high_freq = .0
        high_freq_temp = .0
        low_freq = .0
        low_freq_temp = .0

        for (high, low) in zip(DTMF_HIGH, DTMF_LOW):
            if powers[high] > high_freq_temp:
                high_freq_temp = powers[high]
                high_freq = high

            if powers[low] > low_freq_temp:
                low_freq_temp = powers[low]
                low_freq = low

        for key in DTMF_TABLE:
            if DTMF_TABLE[key][0] == high_freq and DTMF_TABLE[key][1] == low_freq:
                return key

    def calc_s_n(self, sample_data):
        # Вычисляет Sn.
        #
        # Parameters
        # ----------
        # sample_data : частота дикретизации.

        for freq in DTMF_FREQ:
            s = self.coeff[freq] * self.s_prev[freq] - self.s_prev2[freq] + sample_data
            self.s_prev2[freq] = self.s_prev[freq]
            self.s_prev[freq] = s

    def calc_power(self) -> {float: float}:
        # Вычисляет магнитуды частот.
        #
        # Returns
        # -------
        # powers : {float: float}
        #     словарь частот и их магнитуд.

        powers = {}

        for freq in DTMF_FREQ:
            power = self.s_prev2[freq] ** 2 + self.s_prev[freq] ** 2 - \
                    self.coeff[freq] * self.s_prev[freq] * self.s_prev2[freq]
            powers[freq] = power

        return powers

    def reset(self):
        # Удаляет ранее посчитанные данные.

        self.s_prev = {}
        self.s_prev2 = {}

        for k in DTMF_FREQ:
            self.s_prev[k] = .0
            self.s_prev2[k] = .0
