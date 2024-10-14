# sliderplot

![PyPI - Downloads](https://img.shields.io/pypi/dm/sliderplot)

Turn a function into an interactive plot with a single line of code.

It is very similar to [Holoviews DynamicMap](https://holoviews.org/reference/containers/bokeh/DynamicMap.html) but with
multiple lines and
plots capabilities, and with only sliders as interactive elements.

# Demo

<p align="center">
    <img src="https://github.com/ngripon/sliderplot/raw/main/demo.gif" width="520" alt="demo" />
</p>

``` python
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
```

# Features

## Single line

To create a sliderplot with a single line, pass into `sliderplot()` a function that returns same-length `x` and `y`
vectors.

### Example

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f)
```

## Multiple lines

To create a sliderplot with multiple lines, pass into `sliderplot()` a function that returns multiple pairs of
same-length `x` and `y`
vectors.

### Example

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return (x, y), (x, 2 * y), (x, 3 * y)


sliderplot(f)
```

## Multiple subplots

TODO

## Default slider position

TODO

## Slider bounds settings

TODO

## Plot edition

### Axis labels

### Plot title

TODO
