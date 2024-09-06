import enum
import inspect
from inspect import signature
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

SLIDER_HEIGHT = 0.05
BOTTOM_PADDING = (0.03, 0.1)


class PlotMode(enum.Enum):
    LINE_X = 0
    LINE_XY = 1
    MULTI_LINE = 2
    MULTI_PLOT = 3


def sliderplot(f: Callable, params_bounds=(), show: bool = True):
    """
    Create an interactive plot with sliders to explore the outputs of the function f for different inputs.
    :param f: Function to explore.
    :param params_bounds: Sequence of (val_min, val_max) bounds for each parameter of the function f.
    :param show: If True, show the plot.
    :return: fig and axs (Axes object if there is one subplot, and list of Axes if there are multiple subplots).
    """
    # Get init parameters
    params = signature(f).parameters
    init_params = [param.default if param.default is not inspect.Parameter.empty else 1 for param in
                   params.values()]

    outputs = f(*init_params)
    fig, axs, lines, plot_mode = create_plot(outputs)

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(bottom=sum(BOTTOM_PADDING) + len(params) * SLIDER_HEIGHT)

    # Make a horizontal slider to control the frequency.
    sliders = []
    for i, param in enumerate(params.keys()):
        slider_ax = fig.add_axes((0.1, BOTTOM_PADDING[0] + SLIDER_HEIGHT * (len(params) - 1 - i), 0.6, 0.03))
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

        for line, (x, y) in zip(lines, get_lines(outputs, plot_mode)):
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
    reset_ax = fig.add_axes((0.8, BOTTOM_PADDING[0] + (len(params) - 1) * SLIDER_HEIGHT, 0.1, 0.04))
    button = Button(reset_ax, 'Reset', hovercolor='0.975')

    def reset(event):
        [slider.reset() for slider in sliders]

    button.on_clicked(reset)
    fig._sliderplot_button = button  # Prevent garbage collector from deleting button behavior
    if show:
        plt.show()
    return fig, axs


def get_plot_mode(output_data) -> PlotMode:
    plot_mode_map = {1: PlotMode.LINE_X, 2: PlotMode.LINE_XY, 3: PlotMode.MULTI_LINE, 4: PlotMode.MULTI_PLOT}
    depth = compute_depth(output_data)
    if depth in plot_mode_map.keys():
        return plot_mode_map[depth]
    else:
        raise Exception("Failed to transform the output data of the function into plots. "
                        "Please look at the documentation for correct data formatting.")


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
    plot_mode = get_plot_mode(outputs)
    n_plots = len(outputs) if plot_mode is PlotMode.MULTI_PLOT else 1
    fig, axs = plt.subplots(ncols=n_plots)
    if plot_mode is PlotMode.MULTI_PLOT:  # axs is an array of Axes objects
        for ax, subplot_data in zip(axs, outputs):
            ax.grid()
            for x, y in subplot_data:
                line, = ax.plot(x, y, lw=2)
                lines.append(line)
    else:  # axs is an Axes object
        axs.grid()
        if plot_mode is PlotMode.MULTI_LINE:
            for x, y in outputs:
                line, = axs.plot(x, y, lw=2)
                lines.append(line)
        elif plot_mode is PlotMode.LINE_XY:
            line, = axs.plot(outputs[0], outputs[1], lw=2)
            lines.append(line)
        elif plot_mode is PlotMode.LINE_X:
            x = np.arange(len(outputs))
            line, = axs.plot(x, outputs, lw=2)
            lines.append(line)
    return fig, axs, lines, plot_mode


def get_lines(outputs, plot_mode: PlotMode):
    if plot_mode is PlotMode.MULTI_LINE:
        return outputs
    elif plot_mode is PlotMode.LINE_XY:
        return ((outputs[0], outputs[1]),)
    elif plot_mode is PlotMode.LINE_X:
        x = np.arange(len(outputs))
        return ((x, outputs),)
    elif plot_mode is PlotMode.MULTI_PLOT:
        return np.concatenate((*outputs,))
    else:
        raise Exception("Invalid plot_mode argument.")


if __name__ == '__main__':
    def f(k=2, c=3, m=5):
        x = np.linspace(0, 100)
        y = k * x - c + x % m
        return ((x, y),), ((2 * x, 2 * y), (x, 2 * y - x))


    fig, axs = sliderplot(f, show=False)
    axs[0].set_title("Hey")
    plt.show()
