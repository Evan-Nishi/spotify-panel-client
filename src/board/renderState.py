from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
class RenderState:
    def __init__(self, title = '', artists = '', file_name = '', progress = '0', title_font = '5x7', sub_font = '4x6'):
        #TODO convert options to either work from dotenv or with command line args cuz this is unacceptable
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.brightness = 60
        options.parallel = 1
        options.chain_length = 1
        options.hardware_mapping = 'adafruit-hat-pwm'

        matrix = RGBMatrix(options = options)
        
        title_font = graphics.Font('../assets/{}.bdf'.format(title_font))
        title_font.LoadFont()

        sub_font = graphics.Font('../assets/{}.bdf'.format(sub_font))
        sub_font.LoadFont()

        self.title = title
        self.artists = artists
        self.f_name = file_name
        self.prog = progress
        self.matrix = matrix
        self.canvas = self.matrix.CreateFrameCanvas()
        self.sf = sub_font
        self.tf = title_font
        
    def drawText(self):
        return 0

    def render(self):
        self.matrix.SwapOnVSync(self.canvas)
        return 0