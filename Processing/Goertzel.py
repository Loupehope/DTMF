import math
import scipy.io.wavfile

from Helpers.Const import *


class Goertzel:

    def __init__(self, sample_rate: int, bin_size: int):
        self.s_prev = {}
        self.s_prev2 = {}
        self.coeff = {}

        for k in DTMF_FREQ:
            self.s_prev[k] = .0
            self.s_prev2[k] = .0

            freq_k = .5 + (bin_size * k) / sample_rate

            self.coeff[k] = 2.0 * math.cos(2.0 * math.pi * freq_k / bin_size)

    def get_number(self, freqs):
        high_freq = .0
        high_freq_temp = .0
        low_freq = .0
        low_freq_temp = .0

        for (high, low) in zip(DTMF_HIGH, DTMF_LOW):
            if freqs[high] > high_freq_temp:
                high_freq_temp = freqs[high]
                high_freq = high

            if freqs[low] > low_freq_temp:
                low_freq_temp = freqs[low]
                low_freq = low

        for key in DTMF_TABLE:
            if DTMF_TABLE[key][0] == high_freq and DTMF_TABLE[key][1] == low_freq:
                return key

    def run(self, sample, is_last_sample):
        freqs = {}

        for freq in DTMF_FREQ:
            s = self.coeff[freq] * self.s_prev[freq] - self.s_prev2[freq] + sample
            self.s_prev2[freq] = self.s_prev[freq]
            self.s_prev[freq] = s

            if is_last_sample:
                power = self.s_prev2[freq] ** 2 + self.s_prev[freq] ** 2 -\
                        self.coeff[freq] * self.s_prev[freq] * self.s_prev2[freq]
                freqs[freq] = power

        if is_last_sample:
            return self.get_number(freqs)
        else:
            return ""

