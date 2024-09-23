import pytest

from sliderplot import sliderplot
import numpy as np


def test_minimal_example():
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return x, y, "Hey"

    sliderplot(f, params_bounds=((0, 1),), titles=("Minimal example",), page_title="Minimal example")


def test_multiple_lines():
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return (x, y), (2 * x, 2 * y, "Yo")

    sliderplot(f, titles=("Multiple lines",), axes_labels=(('Time', "Something"),))


def test_multiple_plots():
    def f(amplitude=2, frequency=2, phase=2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return ((x, y, "Hey"),), ((x, 2 * y), (x, x + y,"Hop la"))

    sliderplot(f, titles=("Test 1", "Test 2"), axes_labels=(('Time', "Something"), ('Weight', "Anything"),))


def test_lot_of_lines():
    def f(amplitude=2, frequency=2, phase=2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        multi_lines = []
        for i in range(20):
            multi_lines.append((x, i * y))
        return ((x, y),), multi_lines

    sliderplot(f)
