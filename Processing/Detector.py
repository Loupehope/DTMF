from Processing.Goertzel import *


class Detector:

    @staticmethod
    def detect(rate, data):
        result = ""
        bin_size = 400
        bin_size_split = 4
        value = ""
        prev_value = ""
        prev_counter = 0

        for i in range(0, len(data) - bin_size, bin_size // bin_size_split):
            goertzel = Goertzel(rate)

            for j in data[i:i + bin_size]:
                value = goertzel.run(j)

            if value == prev_value:
                prev_counter += 1
                if prev_counter == 10:
                    result += value
            else:
                prev_counter = 0
                prev_value = value

        return result
