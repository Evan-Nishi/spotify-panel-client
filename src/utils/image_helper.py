import re
from PIL import Image

import os
import requests
import shutil

#All file side stuff here

def fetch_img(file_name, url):
    #Fetches image from URL

    #Params:
    #   file_name(str): name of file WITH FILE HEADER
    #   url(str): url to fetch image from

    req = requests.get(url, stream=True)
    if req.status_code == 200:
        try:
            f = open('../assets/{}'.format(file_name), 'wb')
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, f)
            f.close()
        finally:
            pass
        
        return 0
def resize(file_name, h = 32, w = 32):
    #Resizes and replaces image to hxw.  Note file name will have hxw at end after completion.  Defaults to 32x32
    
    #Returns:
    #   string: new file name

    #Params:
    #   file_name(str): name of file WITH FILE HEADER
    #   h(int): height in pixels of resize
    #   w(int): width in pixels of resize

    #IDs as of now don't have periods but may need to change later
    f_split = file_name.split('.')

    #TODO add relative path as env variable 
    if check_cover(file_name):
        with open(r'../assets/{}'.format(file_name),'rb') as f:
            img = Image.open(f)
            f_name = '{}_{}x{}.{}'.format(f_split[0],h,w, f_split[-1])
            resized = img.resize((h,w), resample=Image.BILINEAR)
            resized.save(r'../assets/{}'.format(f_name))

        os.remove('../assets/{}'.format(file_name))
    return f_name
    

def check_cover(file_name):
    #Checks if given cover art exists in assets
    if os.path.exists('../assets/{}'.format(file_name)):
        return True
    else:
        return False


