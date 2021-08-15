import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def config():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.brightness = 60
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat-pwm'
    return options