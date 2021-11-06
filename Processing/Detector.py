from Processing.Goertzel import *


class Detector:

    @staticmethod
    def detect(rate, data):
        result = ""
        bin_size = 205
        value = ""
        prev_value = ""
        prev_counter = 1

        for i in range(0, len(data) - bin_size, bin_size):
            goertzel = Goertzel(rate, bin_size)

            for j in range(bin_size):
                value = goertzel.run(data[i + j], j == (bin_size - 1))

            if value == prev_value:
                prev_counter += 1
                if prev_counter == 9:
                    result += value
            else:
                prev_counter = 1
                prev_value = value

        return result
