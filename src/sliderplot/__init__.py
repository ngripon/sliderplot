import inspect
from collections.abc import Sequence
from inspect import signature
from numbers import Number
from os import path
from typing import Callable

import panel as pn
from bokeh.models import BasicTickFormatter

pn.extension(design="material")

from sliderplot.sliderplot import _BOTTOM_PADDING, _SLIDER_HEIGHT, _get_lines, \
    _create_bokeh_plot

_N_POINTS_PER_SLIDER = 1000


def sliderplot(f: Callable, params_bounds: Sequence[tuple[Number, Number]] = (), titles: Sequence[str] = (),
               axes_labels: Sequence[tuple[str, str]] = (), page_title: str = "Sliderplot", page_logo: str = None,
               show:bool=True):
    """
    Create an interactive plot with sliders to explore the outputs of the function f for different inputs.
    :param f: Function to explore.
    :param params_bounds: Sequence of (val_min, val_max) bounds for each parameter of the function f.
    :param titles:
    :param axes_labels:
    :return: fig and axs (Axes object if there is one subplot, and list of Axes if there are multiple subplots).
    """
    # Get init parameters
    params = signature(f).parameters
    init_params = [param.default if param.default is not inspect.Parameter.empty else 1 for param in
                   params.values()]
    outputs = f(*init_params)

    # Create sliders
    sliders = []
    for i, param in enumerate(params.keys()):
        if i < len(params_bounds):
            val_min, val_max = params_bounds[i]
        else:
            val_min, val_max = 0, 20
        slider = pn.widgets.EditableFloatSlider(value=init_params[i], start=val_min, end=val_max, name=param,
                                                step=(val_max - val_min) / _N_POINTS_PER_SLIDER,
                                                format=BasicTickFormatter(precision=4))
        sliders.append(slider)

    fig, lines_source, plot_mode = _create_bokeh_plot(outputs, titles, axes_labels)

    def simulate(*args):
        try:
            new_outputs = f(*args)
        except ZeroDivisionError:
            return
        for line, (x, y) in zip(lines_source, _get_lines(new_outputs, plot_mode)):
            line.data = dict(x=x, y=y)
        return fig

    curves = pn.bind(simulate, *sliders)

    plot = pn.pane.Bokeh(curves, sizing_mode="stretch_both")

    # Dirty trick to fix bug that make the plot empty when init with multiple plots
    sliders[0].value = init_params[0] + 0.0000000001
    sliders[0].value = init_params[0]

    template = pn.template.MaterialTemplate(
        title=page_title,
        sidebar=sliders,
        main=plot
    )
    if page_logo:
        template.param.update(
            logo=page_logo,
            favicon=page_logo
        )
    if show:
        template.show()
    return template
