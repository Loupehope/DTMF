import scipy.io.wavfile


class Reader:

    @staticmethod
    def read(filename: str):
        return scipy.io.wavfile.read(filename)