from sliderplot import sliderplot
import numpy as np


def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f, params_bounds=((0, 1), (1, 1000), (0, np.pi)))
