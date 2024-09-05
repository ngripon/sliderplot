import inspect
from inspect import signature

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

SLIDER_HEIGHT = 0.05
BOTTOM_PADDING = (0.03, 0.1)


def sliderplot(f, params_bounds=(), x_labels=(), y_labels=(), show=True, wrapper=None):
    params = signature(f).parameters
    init_params = [param.default if param.default is not inspect.Parameter.empty else 1 for param in
                   params.values()]
    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    t, y = f(*init_params)
    line, = ax.plot(t, y, lw=2)
    ax.grid()

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(bottom=sum(BOTTOM_PADDING) + len(params) * SLIDER_HEIGHT)

    # Make a horizontal slider to control the frequency.
    sliders = []
    for i, param in enumerate(params.keys()):
        slider_ax = fig.add_axes([0.1, BOTTOM_PADDING[0] + SLIDER_HEIGHT * (len(params) - 1 - i), 0.6, 0.03])
        if i < len(params_bounds):
            val_min, val_max = params_bounds[i]
        else:
            val_min, val_max = 0, 20
        slider = Slider(
            ax=slider_ax,
            label=param,
            valmin=val_min,
            valmax=val_max,
            valinit=init_params[i],
        )
        sliders.append(slider)

    # The function to be called anytime a slider's value changes
    def update(val):
        try:
            t, y = f(*(slider.val for slider in sliders))
        except ZeroDivisionError:
            t, y = [], []
        line.set_data(t, y)
        fig.canvas.draw_idle()
        ax.relim()
        ax.autoscale_view(True, True, True)

    # register the update function with each slider
    [slider.on_changed(update) for slider in sliders]

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.8, BOTTOM_PADDING[0] + (len(params) - 1) * SLIDER_HEIGHT, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')

    def reset(event):
        [slider.reset() for slider in sliders]

    button.on_clicked(reset)
    if show:
        plt.show()
    return fig, ax


if __name__ == '__main__':
    def f(k=2, c=3, m=5):
        x = np.linspace(0, 100)
        y = k * x - c + x % m
        return x, y


    fig, ax=sliderplot(f, show=False)
    ax.set_title("Hey")
    plt.show()
