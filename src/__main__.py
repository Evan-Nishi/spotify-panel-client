import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from utils.config import config

def run():
    matrix = RGBMatrix(options = config)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)