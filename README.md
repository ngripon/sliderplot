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


def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f)
```

## Multiple lines

To create a sliderplot with multiple lines, pass into `sliderplot()` a function that returns multiple pairs of
same-length `x` and `y` vectors.

### Example

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return (x, y), (x, 2 * y), (x, 3 * y)


sliderplot(f)
```

## Multiple subplots

To create a sliderplot with multiple subplots, pass into `sliderplot()` a function that returns a list with the
following levels, top to bottom:

1. List of subplots.
2. List of lines.
3. Line: `(x, y)` pair of same-length vectors, or `(x, y, label: str)` to add a line label.

### Example

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return ((x, y), (x, 2 * y)), ((x, 3 * y),)


sliderplot(f)
```

## Line labels

To add a label to a line that will be displayed in the plot legend, return the line data with the following format:

`(x, y, label: str)`

### Example

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return (x, y, "First"), (x, 2 * y), (x, 3 * y, "Third")


sliderplot(f)
```

## Initial slider position

To set the slider initial value for a parameter, simply add a default argument to the function.

### Example

In the following example, the initial slider values are:

- `amplitude = 1`
- `frequency = np.pi`
- `phase = np.pi / 2`

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f)
```

## Slider bounds settings

Use the `param_bounds` arguments of the `sliderplot()` function to specify the slider bounds of each parameter. It takes
a list of pairs of `(min_value, max_value)`. 

The first pair contains the bounds of the first argument, the second pair
contains the bounds of the second argument, etc...

### Example

In the following example, the slider bounds are:
- `amplitude = (0, 1)`
- `frequency = (1, 1000)`
- `phase = (0, np.pi)`

``` python
from sliderplot import sliderplot
import numpy as np


def f(amplitude, frequency, phase):
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(frequency * x + phase)
    return x, y


sliderplot(f, params_bounds=((0, 1), (1, 1000), (0, np.pi)))
```

## Plot edition

### Axis labels

### Plot title

TODO
