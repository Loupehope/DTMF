from Processing.Goertzel import *


class Detector:

    @staticmethod
    def detect(rate, data) -> str:
        result = ""
        bin_size = 205
        value = ""
        prev_value = ""
        prev_counter = 1
        goertzel = Goertzel(rate, bin_size)

        for i in range(0, len(data) - bin_size, bin_size):
            goertzel.reset()

            for j in range(bin_size):
                goertzel.calc_s_n(data[i + j])

            powers = goertzel.calc_power()
            symbol = goertzel.get_number(powers)

            if symbol == prev_value:
                prev_counter += 1
                if prev_counter == 9:
                    result += symbol
                    prev_counter = 1
            else:
                prev_counter = 1
                prev_value = symbol

        return result
