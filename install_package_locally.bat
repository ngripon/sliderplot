call .venv\Scripts\activate.bat

pip uninstall sliderplot -y
python -m build
pip install dist/sliderplot-0.0.1.tar.gz