from Helpers.Const import *

import math
import numpy as np



class Detector:

    @staticmethod
    def detect(rate: int, data):
        # Calculate fourier transform of data
        f = map(lambda x: (x[1], x[0]), DTMF_TABLE.values())
        freqs, results = Detector.goertzel(data, rate, f)
        print(freqs)
        print(np.array(results)[:, 2])

        # Calculate lower bound for filtering fourier trasform numbers
        lower_bound = 20 * np.average(fourier_transform_data)

        # Filter fourier transform data (only select frequencies that X(jw) is greater than LowerBound)
        filtered_frequencies = []

        for i in range(len(fourier_transform_data)):
            if fourier_transform_data[i] > lower_bound:
                filtered_frequencies.append(i)

        # Detect and print pressed button
        for char, frequency_pair in DTMF_TABLE.items():
            print(char)

    @staticmethod
    def goertzel(samples, sample_rate, freqs):
        window_size = len(samples)
        f_step = sample_rate / float(window_size)
        f_step_normalized = 1.0 / window_size

        # Calculate all the DFT bins we have to compute to include frequencies in `freqs`.
        bins = set()
        for f_range in freqs:
            f_start, f_end = f_range
            k_start = int(math.floor(f_start / f_step))
            k_end = int(math.ceil(f_end / f_step))

            if k_end > window_size - 1:
                raise ValueError('frequency out of range %s' % k_end)
            bins = bins.union(range(k_start, k_end))

        # For all the bins, calculate the DFT term
        n_range = range(0, window_size)
        freqs = []
        results = []

        for k in bins:
            # Bin frequency and coefficients for the computation
            f = k * f_step_normalized
            w_real = 2.0 * math.cos(2.0 * math.pi * f)
            w_imag = math.sin(2.0 * math.pi * f)

            # Doing the calculation on the whole sample
            d1, d2 = 0.0, 0.0
            for n in n_range:
                y = samples[n] + w_real * d1 - d2
                d2, d1 = d1, y

            # Storing results `(real part, imag part, power)`
            results.append((
                0.5 * w_real * d1 - d2, w_imag * d1,
                d2 ** 2 + d1 ** 2 - w_real * d1 * d2)
            )
            freqs.append(f * sample_rate)

        return freqs, results