import collections.abc
import inspect
from inspect import signature

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

SLIDER_HEIGHT = 0.05
BOTTOM_PADDING = (0.03, 0.1)


def sliderplot(f, params_bounds=(), x_labels=(), y_labels=(), titles=(), show=True, wrapper=None):
    # Get init parameters
    params = signature(f).parameters
    init_params = [param.default if param.default is not inspect.Parameter.empty else 1 for param in
                   params.values()]

    outputs = f(*init_params)
    fig, axs, lines = create_plot(outputs)

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
    def update(_):
        try:
            outputs = f(*(slider.val for slider in sliders))
        except ZeroDivisionError:
            return

        for line, (x, y) in zip(lines, get_lines(outputs)):
            line.set_data(x, y)
        fig.canvas.draw_idle()
        if hasattr(axs, "__len__"):
            [ax.relim() for ax in axs]
            [ax.autoscale_view(True, True, True) for ax in axs]
        else:
            axs.relim()
            axs.autoscale_view(True, True, True)

    # register the update function with each slider
    [slider.on_changed(update) for slider in sliders]

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.8, BOTTOM_PADDING[0] + (len(params) - 1) * SLIDER_HEIGHT, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')

    def reset(event):
        [slider.reset() for slider in sliders]

    button.on_clicked(reset)
    fig._sliderplot_button = button  # Prevent garbage collector from deleting button behavior
    if show:
        plt.show()
    return fig, axs


def compute_depth(data) -> int:
    # TODO: check depth of all elements
    depth = 0
    current_element = data
    while True:
        try:
            current_element = current_element[0]
            depth += 1
        except IndexError:
            break
    return depth


def create_plot(outputs):
    lines = []
    outputs_depth = compute_depth(outputs)
    n_plots = 1 if outputs_depth < 4 else len(outputs)
    fig, axs = plt.subplots(ncols=n_plots)
    if n_plots == 1:
        axs.grid()
        if outputs_depth == 3:
            for x, y in outputs:
                line, = axs.plot(x, y, lw=2)
                lines.append(line)
        elif outputs_depth == 2:
            line, = axs.plot(outputs[0], outputs[1], lw=2)
            lines.append(line)
        elif outputs_depth == 1:
            x = np.arange(len(outputs))
            line, = axs.plot(x, outputs, lw=2)
            lines.append(line)
    else:
        for ax, subplot_data in zip(axs, outputs):
            ax.grid()
            for x, y in subplot_data:
                line, = ax.plot(x, y, lw=2)
                lines.append(line)
    return fig, axs, lines


def get_lines(outputs):
    outputs_depth = compute_depth(outputs)
    if outputs_depth == 3:
        return outputs
    elif outputs_depth == 2:
        return ((outputs[0], outputs[1]),)
    elif outputs_depth == 1:
        x = np.arange(len(outputs))
        return ((x, outputs),)
    elif outputs_depth == 4:
        lines_xy = []
        for subplot_data in outputs:
            for x, y in subplot_data:
                lines_xy.append((x, y))
        return lines_xy


if __name__ == '__main__':
    def f(k=2, c=3, m=5):
        x = np.linspace(0, 100)
        y = k * x - c + x % m
        return ((x, y),), ((2 * x, 2 * y), (x, 2 * y - x))


    fig, axs = sliderplot(f, show=False)
    axs[0].set_title("Hey")
    plt.show()
