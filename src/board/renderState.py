from PIL import Image, ImageDraw
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class RenderState:
    def __init__(self, title = '', artists = '', file_name = '', progress = 0, t_font = '5x7', s_font = '4x6', blank = True):
        '''
        Class object that represents the board 

        Attr:
            title(string): title of album cover
            artists(string): comma seperated string of artist(s)
            file_name(string): name of file WITH HEADER
            progress(int): progress (progress_ms/duration_ms) * 100 rounded (percent of song completion)
            t_font(string): {height}x{width} string of font of title that corresponds to a .bdf file in /assets
            s_font(string): {height}x{width} string of font of sub header that corresponds to a .bdf file in /assets
            blank(bool): if request returns 204, song is not playing and board will be blank
        '''
        #TODO convert options to either work from dotenv or with command line args or from config.json
        options = RGBMatrixOptions()

        options.rows = 32
        options.cols = 64
        options.brightness = 90
        options.parallel = 1
        options.chain_length = 1
        options.hardware_mapping = 'adafruit-hat-pwm'
        options.row_address_type = 0
        options.pwm_bits = 11
        options.multiplexing = 0
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = 'RGB'
        options.pixel_mapper_config = ''
        options.panel_type = ''
        options.drop_privileges = False
        options.gpio_slowdown = 1

        self.title_font = graphics.Font()
        self.title_font.LoadFont('../fonts/{}.bdf'.format(t_font))
        
        self.sub_font = graphics.Font()
        self.sub_font.LoadFont('../fonts/{}.bdf'.format(s_font))

        self.title = title
        self.artists = artists
        self.f_name = file_name
        self.prog = progress
        self.matrix = RGBMatrix(options = options)
        self.canvas = self.matrix.CreateFrameCanvas()
        self.blank = True
        self.thread_stop = False
        self.img_obj = None

        self.bar_color = graphics.Color(30, 220, 80)
        self.bar_bg = graphics.Color(130, 130, 130)

        self.t_color = graphics.Color(222, 222, 222)
        self.s_color = graphics.Color(190, 190, 190)

    def set_file(self, new_f_name):
        '''
        stores file object in class 

        Attr:
            new_f_name(str): new name of file
        '''
        self.f_name = new_f_name
        self.img_obj = Image.open('../assets/{}'.format(self.f_name)).convert('RGB')
        return 0

    def draw_prog_bar (self):
        '''
        draws progress bar to self.canvas
        '''
        
        bar_loc = round(36 + int(self.prog) * 0.24)
        #this needs some documentation and to stop using hard coded vals
        graphics.DrawLine(self.canvas, 36, 28, bar_loc, 28, self.bar_color)
        graphics.DrawLine(self.canvas, 36, 29, bar_loc, 29, self.bar_color)
        if(self.prog * 0.24 <= 24):
            graphics.DrawLine(self.canvas, bar_loc + 1, 28, 60, 28, self.bar_bg)
            graphics.DrawLine(self.canvas, bar_loc + 1, 29, 60, 29, self.bar_bg)
        return 0

            

    #TODO switch off hardcoded values
    def render(self):
        '''
        renders board on vertical sync
        '''
        time.sleep(3)
        title_x = 34
        artist_x = 34
        while(self.thread_stop != True):
            if(self.blank or self.img_obj == None):
                self.matrix.Clear()
            else:
                #TODO: have y pos change based on font size
                title_len = graphics.DrawText(self.canvas, self.title_font, title_x, 10, self.t_color, self.title)
                #both title/artist going at same speed is kinda ugly tbh

                #TODO: stagger title and author with second thread
                artist_len = graphics.DrawText(self.canvas, self.sub_font, artist_x, 20, self.s_color , '-' + self.artists)
                
                if(title_len > 32):
                    title_x -= 1
                else:
                    title_x = 34

                if(artist_len > 32):
                    artist_x -= 1
                else:
                    artist_x = 34

                if(title_x + title_len < 18):
                    title_x = 34
                    artist_x = 34

                if(artist_x + artist_len < 18):
                     title_x = 34
                     artist_x = 34

                #only way to get stop effect for text
                #will sleep rest of render 
                if(title_x == 32):
                    time.sleep(2)

                
                self.draw_prog_bar()
                self.canvas.SetImage(self.img_obj, unsafe=False)
                self.canvas = self.matrix.SwapOnVSync(self.canvas)

                time.sleep(0.01)
                self.canvas.Clear()
                
        return 0