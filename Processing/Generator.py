from Models.GarmonikModel import *
from Drivers.ModelDriver import *
from Models.Signal import *

from Helpers.Const import *


class Generator:

    @staticmethod
    def generate_from(symbols: str, duration=.25, volume=.25, rate=8000) -> [Signal]:
        generated = []

        for symbol in symbols:
            generated.append(Generator.calculate(symbol, duration, volume, rate))

        return generated

    @staticmethod
    def calculate(symbol: str, duration=.25, volume=.25, rate=8000) -> Signal:
        first_garmonik = GarmonikModel(volume, DTMF_TABLE[symbol.upper()][0], 0, int(duration * rate), 1, 1 / rate)\
            .trend(0, None)
        second_garmonik = GarmonikModel(volume, DTMF_TABLE[symbol.upper()][1], 0, int(duration * rate), 1, 1 / rate)\
            .trend(0, None)
        final_garmnonik = ModelDriver.add(first_garmonik, second_garmonik)

        return Signal(final_garmnonik, symbol, rate)
