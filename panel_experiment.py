from sliderplot import sliderplot
import numpy as np


def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y, "Hey"


sliderplot(
    f,
    params_bounds=((0, 1),),
    titles=("Minimal example",),
    page_title="Minimal example",
)
