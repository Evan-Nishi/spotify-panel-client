from base64 import b64encode
import requests
#expired access token: BQDv10stdjKOBQ_vuELX16NSx0Djhi0xwiIGH3aZxgkJ_F4nxt2bOip4mXtzVzNTqTy8tuaqs-5aLE953SvU11hQWX09wYrNk2Qeue5ViO3UQQa5JqxuUrZAENza9zIyjpwnVMSjcDMDggH7fBl3HyJESM-nsymtdUWLBXsUArzZmg

def curr_track(access_token):
    #Returns current track as JSON object

    #Params:
    #   access_token(str): access token obtained from ./auth.py

    #Returns:
    #   JSON object: response object with curr track info OR 204 if empty

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    req = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)

    if req.status_code == 204:
        return 204
    return req