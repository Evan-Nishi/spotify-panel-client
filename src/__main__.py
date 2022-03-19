import sys
import threading #yk this is gonna be bad
import os
import time

import utils.image_helper as img_h
#import board.renderState as r
import api.auth as auth
import api.dao as dao
from dotenv import load_dotenv, find_dotenv


def run():
    load_dotenv(find_dotenv())

    #TODO: this delay system is horrendous as it will give different delays based
    #on hardware performance between cycles instead of a fixed time given by TIMEOUT
    #TODO: switch buffer, timeout, and inactive_timeout to config.json instead of dotenv

    #buffer delay between cycles in seconds, for rate limit purposes have it greater than 0.3s
    BUFFER = float(os.environ.get('CYCLE_BUFFER'))
    #board timeout in cycles(roughly 0.1s + delay buffer), set to -1 for no timeout, must be whole number
    TIMEOUT = int(os.environ.get('TIMEOUT'))
    #inactive timeout in cycles(roughly 0.1s + delay buffer), set to -1 for no inactive timeout, must be whole number
    INACTIVE_TIMEOUT = int(os.environ.get('INACTIVE_TIMEOUT'))

    TOKEN = os.environ.get('REF_TOKEN')
    SECRET = os.environ.get('CLIENT_SECRET')
    ID = os.environ.get('CLIENT_ID')

    iter = 0
    inactive_count = 0

    access_token = auth.get_access_token(TOKEN, ID, SECRET)
   
    #time until token expires w 10 sec buffer
    #TODO get expire time from api instead of hard coded val even though it is constant
    expire = time.time() + 3590

    #board_state = r.RenderState()

    #NOTE this thread should not modify board_state under ANY circumstances
    
    #render_thread = threading.Thread(target=board_state.render)
    #render_thread.start()
    
    
    #should probably make ErrorHandler class but I lazy
    while (TIMEOUT - iter != 0 and INACTIVE_TIMEOUT - inactive_count != 0):
        req = dao.curr_track(access_token)

        #CHECKS FOR THE SAME THING TWICE IDIOT
        if(req != 204):
            curr_track = req.json()
        
        if(time.time() >= expire):
            access_token = auth.get_access_token(TOKEN, ID, SECRET)
            expire = time.time() + 3590
        try:
            status = curr_track['error']['status']
            if(status == 401):
                #for redundancy in case expire time changes, may remove later
                print('Status: ' + str(curr_track['error']['status']) + ' access token expired requesting new')
                access_token = auth.get_access_token(TOKEN, ID, SECRET)
            elif(status == 429):
                #if rate limit exceeded, deploy back-off retry
                print('Status: ' + str(curr_track['error']['status']) + 'rate limit exceeded retry in ' + str(curr_track['error']['Retry-After']))
                time.sleep(curr_track['error']['Retry-After'])
        except:
            pass

        #TODO refactor, this is horrendous and I shouldn't be a programmer
        if(req != 204):
            #board_state.blank = False
            inactive_count = 0
            album_id = curr_track['item']['album']['id']

            #gets smallest resolution (64x64) image and fetches it
            img_h.fetch_img(album_id + '.jpg', curr_track['item']['album']['images'][-1]['url'])
            f_name = img_h.resize(album_id + '.jpg')
            
            artist_string = ''

            #if multiple authors, get all and comma seperate
            for a in curr_track['item']['album']['artists']:
                artist_string += a['name'] + ', '
            artist_string = artist_string[0:-2]
            
            print(round(curr_track['progress_ms']/curr_track['item']['duration_ms'] * 100))
            #board_state.artists = artist_string
            #board_state.title = curr_track['item']['album']['name']
            #board_state.set_file(f_name)
            iter += 1
        else:
            #board_state.blank = True
            inactive_count += 1
        time.sleep(BUFFER)

    #board_state.thread_stop = True
    return 0
        


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Exiting')
        sys.exit(0)