import time

import numpy as np
import panel as pn
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("agg")
pn.extension()

def display_plot(k):
    x = np.linspace(0, 10, 101)
    y = k * x
    time.sleep(k/10)
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(x, y)
    ax.grid()
    plt.close(fig)
    component = pn.pane.Matplotlib(fig, format="svg", tight=True, sizing_mode="stretch_width")
    return component


slider=pn.widgets.FloatSlider(value=1, start=-10, end=25, step=1, name="hey")

plot=pn.bind(display_plot, k=slider)


pn.Row(slider, plot).show()
