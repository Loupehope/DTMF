import math
import scipy.io.wavfile

from Helpers.Const import *


class Goertzel:

    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.s_prev = {}
        self.s_prev2 = {}
        self.total_power = {}
        self.N = {}
        self.coeff = {}

        for k in DTMF_FREQ:
            self.s_prev[k] = 0.0
            self.s_prev2[k] = 0.0
            self.total_power[k] = 0.0
            self.N[k] = 0.0

            normalized_freq = k / self.sample_rate

            self.coeff[k] = 2.0 * math.cos(2.0 * math.pi * normalized_freq)

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

    def run(self, sample):
        freqs = {}

        for freq in DTMF_FREQ:
            s = self.coeff[freq] * self.s_prev[freq] - self.s_prev2[freq] + sample

            self.s_prev2[freq] = self.s_prev[freq]
            self.s_prev[freq] = s
            self.N[freq] += 1

            power = self.s_prev2[freq] ** 2 + self.s_prev[freq] ** 2 - self.coeff[freq] * self.s_prev[freq] * self.s_prev2[freq]

            self.total_power[freq] += sample ** 2

            if self.total_power[freq] == 0:
                self.total_power[freq] = 1

            freqs[freq] = power / self.total_power[freq] / self.N[freq]

        return self.get_number(freqs)
