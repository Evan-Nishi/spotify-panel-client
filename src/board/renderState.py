from PIL import Image
from matplotlib.pyplot import title
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class RenderState:
    def __init__(self, title = '', artists = '', file_name = '', progress = '0', title_font = '5x7', sub_font = '4x6', blank = True):
        '''
        Class object that represents the board 

        Attr:
            title(string): title of album cover
            artists(string): comma seperated string of artist(s)
            file_name(string): name of file WITH HEADER
            progress(int): progress (progress_ms/duration_ms) * 100 rounded 
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
        
        title_font = graphics.Font('../fonts/{}.bdf'.format(title_font))
        title_font.LoadFont()

        sub_font = graphics.Font('../fonts/{}.bdf'.format(sub_font))
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
        self.thread_stop = False

        self.bar_color = graphics.Color(30, 220, 80)
        self.bar_bg = graphics.Color(130, 130, 130)
        self.white = graphics.Color(255, 255, 255)

    def draw_prog_bar (self):
        '''
        draws progress bar
        '''
        '''
        red = graphics.Color(255, 0, 0)
        graphics.DrawLine(canvas, 5, 5, 22, 13, red)

        green = graphics.Color(0, 255, 0)
        graphics.DrawCircle(canvas, 15, 15, 10, green)
        '''
        #this needs some explanation and to stop using hard coded vals
        graphics.DrawLine(self.canvas, 36, 8, (36 + self.prog * 24), 8, self.bar_color)
        graphics.DrawLine(self.canvas, 36, 9, (36 + self.prog * 24), 9, self.bar_color)
        if(self.prog * 24 < 24):
            graphics.DrawLine(self.canvas, (36 + self.prog * 24), 8, 60, 8, self.bar_bg)
            graphics.DrawLine(self.canvas, (36 + self.prog * 24), 9, 60, 9, self.bar_bg)
        return 0
        
    def draw_text(self, x_pos, y_pos, color, text, font):
        '''
        draws text of board
        
        Args:
            x_pos(int): x position of text
            y_pos(int): y position of text
            color(object): rgb colors of text in graphics.Color object
            text(string): text to be rendered
            font(Font): graphics.Font object of font
        '''
        graphics.DrawText(self.canvas, font, x_pos, y_pos, color, text)
        return 0
    
    def draw_image(self):
        img = Image.open(self.file_name)
        self.matrix.SetImage(img.convert('RGB'))
        return 0
    
    #TODO switch off hardcoded values
    def render(self):
        '''
        renders board on vertical sync
        '''
        title_x = 30
        artist_x = 30
        while(self.thread_stop != True):
            if(self.blank):
                self.canvas.Clear()
            else:
                title_len = graphics.DrawText(self.canvas, self.tf, title_x, 10, self.title)
                artist_len = graphics.DrawText(self.canvas, self.sf, artist_x, 20, self.artists)
                
                if(title_len >= 28):
                    title_x += 1

                if(artist_len >= 28):
                    title_x += 1
                self.draw_image()
                self.draw_prog_bar()

                time.sleep(0.05)
                self.matrix.SwapOnVSync(self.canvas)
        return 0