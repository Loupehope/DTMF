from Processing.Goertzel import *
from Models.AmpF import *

from Helpers.Const import *

import numpy as np

class Detector:

    @staticmethod
    def simple_detector(rate, symbol_length, data) -> str:
        dt = 1 / rate
        chunk_step = int(symbol_length * rate)
        spectrums = []

        for i in range(0, len(data[1]), chunk_step):
            chunk = [data[0][i:i + chunk_step], data[1][i:i + chunk_step]]
            spectrum = AmpF.calc(chunk, dt, 1)
            spectrums.append([spectrum[0].copy(), spectrum[1].copy()])

        f_s = []

        for i in range(len(spectrums)):
            spectrum = spectrums[i]
            first_max_amp = -9999999
            first_max = 0
            second_max_amp = -9999999
            second_max = 0

            for j in range(len(spectrum[0])):
                if first_max_amp < spectrum[1][j]:
                    first_max = spectrum[0][j]
                    first_max_amp = spectrum[1][j]

            for j in range(len(spectrum[0])):
                if second_max_amp < spectrum[1][j] and spectrum[1][j] != first_max_amp:
                    second_max = spectrum[0][j]
                    second_max_amp = spectrum[1][j]

            f_s.append(sorted([first_max, second_max]))

        result = ""

        for i in f_s:
            print(i)
            numb = Detector.get_number(i[1], i[0])
            if numb is not None:
                result += numb
        return result

    @staticmethod
    def get_number(first_max, second_max):
        high_freq = .0
        low_freq = .0

        for (high, low) in zip(DTMF_HIGH, DTMF_LOW):
            if high - 10 <= first_max <= high + 10:
                high_freq = high

            if low - 10 <= second_max <= low + 10:
                low_freq = low

        for key in DTMF_TABLE:
            if DTMF_TABLE[key][0] == high_freq and DTMF_TABLE[key][1] == low_freq:
                return key
        return None

    @staticmethod
    def detect(rate, data) -> str:
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
