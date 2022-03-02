import sys
import api.auth as auth
import api.dao as dao
import os
import time

#from rgbmatrix import RGBMatrix, RGBMatrixOptions
#from utils.config import config
from dotenv import load_dotenv, find_dotenv


def run():
    load_dotenv(find_dotenv())

    #buffer delay between cycles 
    BUFFER = 0.8

    #board timeout in cycles(roughly 0.2s + delay), set to -1 for no timeout
    TIMEOUT = 8000

    #inactive timeout in cycles(roughly 0.2s + delay), set to -1 for no incactive timeout
    INACTIVE_TIMEOUT = 1000

    iter = 0
    inactive_count = 0

    TOKEN = os.environ.get('REF_TOKEN')
    SECRET = os.environ.get('CLIENT_SECRET')
    ID = os.environ.get('CLIENT_ID')

    #used to check if entire board needs to be rerendered or just part
    prev_id = 0

    #matrix = RGBMatrix(options = config)
    access_token = auth.get_access_token(TOKEN, ID, SECRET)['access_token']
   
    #time until token expires w 10 sec buffer
    expire = time.time() + 3590

    #should probably make ErrorHandler class but I lazy
    while (TIMEOUT - iter == 0 or INACTIVE_TIMEOUT - inactive_count == 0):
        res = dao.curr_track(access_token)

        if(time.time() >= expire):
            access_token = auth.get_access_token(TOKEN, ID, SECRET)
            expire += 3590

        try:
            status = res['error']['status']
            if(status == 401):
                #redundancy
                print('Status: ' + str(res['error']['status']) + ' access token expired requesting new')
                access_token = auth.get_access_token(TOKEN, ID, SECRET)
            elif(status == 429):
                #if rate limit exceeded, deploy back-off retry
                print('Status: ' + str(res['error']['status']) + 'rate limit exceeded retry in ' + str(res['error']['Retry-After']))
                time.sleep(res['error']['Retry-After'])
        except NameError:
            pass

        if res != 204:
            curr_track = dao.curr_track(access_token)
            iter += 1

        else:
            inactive_count += 1

            #render_board()
        time.sleep(BUFFER)
    return 0
        


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Exiting')
        sys.exit(0)