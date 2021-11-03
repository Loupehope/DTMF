from Models.GarmonikModel import *
from Drivers.ModelDriver import *
from Models.Signal import *

from Helpers.Const import *


class Generator:

    @staticmethod
    def parse_and_generate(symbols: [str], duration=.25, volume=.25, rate=44100) -> [Signal]:
        generated = []

        for symbol in symbols:
            generated.append(Generator.generate(symbol, duration, volume, rate))

        return generated

    @staticmethod
    def generate(symbol: str, duration=.25, volume=.25, rate=44100) -> Signal:
        first_garmonik = GarmonikModel(volume, DTMF_TABLE[symbol.upper()][0], 0, int(duration * rate), 1, 1 / rate)\
            .trend(0, None)
        second_garmonik = GarmonikModel(volume, DTMF_TABLE[symbol.upper()][1], 0, int(duration * rate), 1, 1 / rate)\
            .trend(0, None)
        final_garmnonik = ModelDriver.add(first_garmonik, second_garmonik)

        return Signal(final_garmnonik, symbol, rate)
