import scipy.io.wavfile


class Reader:

    @staticmethod
    def read(filename: str):
        # Читает wav файл.
        #
        # Parameters
        # ----------
        # filename : путь к файлу.
        #
        # Returns
        # -------
        # rate : int
        #     Частота дискретизации.
        # data : numpy array
        #     Данные файла.

        return scipy.io.wavfile.read(filename)
