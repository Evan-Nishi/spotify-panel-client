from tkinter import font

from matplotlib.pyplot import text
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
class RenderState:
    def __init__(self, title = '', artists = '', file_name = '', progress = '0', title_font = '5x7', sub_font = '4x6', blank = True):
        '''
        Class object that represents the board 

        Attr:
            title(string): title of album cover
            artists(string): comma seperated string of artist(s)
            file_name(string): name of file WITH HEADER
            progress(int): progress in percent of song completion
            title_font(string): {height}x{width} string of font of title that corresponds to a .bdf file in /assets
            sub_font(string): {height}x{width} string of font of sub header that corresponds to a .bdf file in /assets
            blank(bool): if request returns 204, song is not playing and board will be blank
        '''
        #TODO convert options to either work from dotenv or with command line args
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
        self.blank = True
        
    def draw_text(self, x_pos, y_pos, color, text, font):
        '''
        draws text of board
        
        Args:
            x_pos(int): x position of text
            y_pos(int): y position of text
            color(array): rgb colors of text
            text(string): text to be rendered
            font(Font): graphics.Font object of font
        '''
        t_color = graphics.Color(color[0],color[1],color[2])
        graphics.DrawText(self.canvas, font, x_pos, y_pos, t_color, text)
        return 0
    def draw_image(self):
        return 0

    def render(self):
        '''
        renders board on vertical sync
        '''
        if(self.blank):
            self.canvas.Clear()
        self.matrix.SwapOnVSync(self.canvas)
        return 0