from IO.Write import *
from IO.Reader import *

from Processing.Generator import *
from Processing.Detector import *
from Processing.Goertzel import *

from Drivers.ModelDriver import *
from Models.RandomModel import *
from Models.AmpF import *
from Models.Filters import *

from Drivers.SpecInfoDisplayDriver import *

import tkinter as tk


if __name__ == '__main__':
    # Устанавливаем окно и обьект графиков
    window = tk.Tk()
    window.title("Методы обработки экспериментальных данных")
    display_model = SpecInfoDisplayDriver(window)

    # ---------------
    # Данные на входе
    file_path = "/Users/vladsuhomlinov/DTMF/sound.wav"
    numbers = '147*'

    # ---------------
    # Записываем
    symbols = Generator.generate_from(numbers, 0.25, 0.5, 8000)
    Writer.write(file_path, symbols)

    # ---------------
    # Считываем
    rate, data = Reader.read(file_path)

    # detected = Detector.simple_detector(rate, .25, data)
    #
    # print("Распознано для " + numbers + ": " + detected)

    # Запускаем
    x_array = []
    y_array = data.copy()
    dt = 1 / rate
    x = 0

    for i in range(len(data)):
        x_array.append(x)
        x += dt

    random_noize = RandomModel(-6, 6, 0, len(data), 1, dt).trend()
    y_array = ModelDriver.add(random_noize, [[], y_array])[1]
    filter = Filters.bpw_filter(659, 1700, dt, 64)
    # len = ModelDriver.convolution([x_array, y_array], filter, dt)

    detected = Detector.detect(rate, y_array)
    print("Распознано: " + detected)

    # chunk = int(.25 * rate)
    #
    # random_noize = RandomModel(-2, 2, 0, len(data), 1, dt).trend()
    # y_array = ModelDriver.add(random_noize, [[], y_array])[1]
    #
    # detected = Detector.detect(rate, y_array)
    # print("Распознано для " + numbers + ": " + detected)
    #
    # chunks = []
    # for i in range(0, len(y_array), chunk):
    #     first = [x_array[i:i+chunk], y_array[i:i+chunk]]
    #     second = AmpF.calc(first, dt, 1)
    #     chunks.append([first, second])

    first = [x_array, y_array]
    #
    # random_noize = RandomModel(-1, 1, 0, len(data), 1, dt).trend()
    # first = ModelDriver.add(first, random_noize)


    second = AmpF.calc(first, dt, 1)

    display_model.plot(first, "Символы: " + numbers)
    display_model.plot(second, "Спектр: " + numbers, "Гц", "")
    # display_model.plot(chunks[0][0], "Символы: " + "*")
    # display_model.plot(chunks[0][1], "Спектр: *", "Гц", "")
    display_model.display()
    window.mainloop()

    print('Успех!')
