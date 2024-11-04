from sliderplot import sliderplot
import numpy as np


def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return ((x, y), (x, 2 * y)), ((x, 3 * y),)


sliderplot(f, page_title="Page title")
